import logging
import socket
import textwrap
from datetime import datetime
from functools import lru_cache, wraps
from time import sleep
from typing import ClassVar, Optional, Tuple

from paramiko import (
    AutoAddPolicy,
    Channel,
    ECDSAKey,
    Ed25519Key,
    PKey,
    RSAKey,
    SSHClient,
    SSHException,
    ssh_exception,
)
from paramiko.ssh_exception import AuthenticationException

from frostfs_testlib.reporter import get_reporter
from frostfs_testlib.shell.interfaces import CommandInspector, CommandOptions, CommandResult, Shell

logger = logging.getLogger("frostfs.testlib.shell")
reporter = get_reporter()


class HostIsNotAvailable(Exception):
    """Raised when host is not reachable via SSH connection."""

    def __init__(self, host: str = None):
        msg = f"Host {host} is not available"
        super().__init__(msg)


def log_command(func):
    @wraps(func)
    def wrapper(
        shell: "SSHShell", command: str, options: CommandOptions, *args, **kwargs
    ) -> CommandResult:
        command_info = command.removeprefix("$ProgressPreference='SilentlyContinue'\n")
        with reporter.step(command_info):
            logger.info(f'Execute command "{command}" on "{shell.host}"')

            start_time = datetime.utcnow()
            result = func(shell, command, options, *args, **kwargs)
            end_time = datetime.utcnow()

            elapsed_time = end_time - start_time
            log_message = (
                f"HOST: {shell.host}\n"
                f"COMMAND:\n{textwrap.indent(command, ' ')}\n"
                f"RC:\n {result.return_code}\n"
                f"STDOUT:\n{textwrap.indent(result.stdout, ' ')}\n"
                f"STDERR:\n{textwrap.indent(result.stderr, ' ')}\n"
                f"Start / End / Elapsed\t {start_time.time()} / {end_time.time()} / {elapsed_time}"
            )

            if not options.no_log:
                logger.info(log_message)

            reporter.attach(log_message, "SSH command.txt")
        return result

    return wrapper


@lru_cache
def _load_private_key(file_path: str, password: Optional[str]) -> PKey:
    """Loads private key from specified file.

    We support several type formats, however paramiko doesn't provide functionality to determine
    key type in advance. So we attempt to load file with each of the supported formats and then
    cache the result so that we don't need to figure out type again on subsequent calls.
    """
    logger.debug(f"Loading ssh key from {file_path}")
    for key_type in (Ed25519Key, ECDSAKey, RSAKey):
        try:
            return key_type.from_private_key_file(file_path, password)
        except SSHException as ex:
            logger.warn(f"SSH key {file_path} can't be loaded with {key_type}: {ex}")
            continue
    raise SSHException(f"SSH key {file_path} is not supported")


class SSHShell(Shell):
    """Implements command shell on a remote machine via SSH connection."""

    # Time in seconds to delay after remote command has completed. The delay is required
    # to allow remote command to flush its output buffer
    DELAY_AFTER_EXIT = 0.2

    SSH_CONNECTION_ATTEMPTS: ClassVar[int] = 3
    CONNECTION_TIMEOUT = 90

    def __init__(
        self,
        host: str,
        login: str,
        password: Optional[str] = None,
        private_key_path: Optional[str] = None,
        private_key_passphrase: Optional[str] = None,
        port: str = "22",
        command_inspectors: Optional[list[CommandInspector]] = None,
    ) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.private_key_path = private_key_path
        self.private_key_passphrase = private_key_passphrase
        self.command_inspectors = command_inspectors or []
        self.__connection: Optional[SSHClient] = None

    @property
    def _connection(self):
        if not self.__connection:
            self.__connection = self._create_connection()
        return self.__connection

    def drop(self):
        self._reset_connection()

    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        options = options or CommandOptions()

        for inspector in self.command_inspectors:
            command = inspector.inspect(command)

        if options.interactive_inputs:
            result = self._exec_interactive(command, options)
        else:
            result = self._exec_non_interactive(command, options)

        if options.check and result.return_code != 0:
            raise RuntimeError(
                f"Command: {command}\nreturn code: {result.return_code}\nOutput: {result.stdout}"
            )
        return result

    @log_command
    def _exec_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        stdin, stdout, stderr = self._connection.exec_command(
            command, timeout=options.timeout, get_pty=True
        )
        for interactive_input in options.interactive_inputs:
            input = interactive_input.input
            if not input.endswith("\n"):
                input = f"{input}\n"
            try:
                stdin.write(input)
            except OSError:
                logger.exception(f"Error while feeding {input} into command {command}")

        if options.close_stdin:
            stdin.close()
        sleep(self.DELAY_AFTER_EXIT)

        decoded_stdout, decoded_stderr = self._read_channels(stdout.channel, stderr.channel)
        return_code = stdout.channel.recv_exit_status()

        result = CommandResult(
            stdout=decoded_stdout,
            stderr=decoded_stderr,
            return_code=return_code,
        )
        return result

    @log_command
    def _exec_non_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        try:
            stdin, stdout, stderr = self._connection.exec_command(command, timeout=options.timeout)

            if options.close_stdin:
                stdin.close()

            decoded_stdout, decoded_stderr = self._read_channels(stdout.channel, stderr.channel)
            return_code = stdout.channel.recv_exit_status()

            return CommandResult(
                stdout=decoded_stdout,
                stderr=decoded_stderr,
                return_code=return_code,
            )
        except (
            SSHException,
            TimeoutError,
            ssh_exception.NoValidConnectionsError,
            ConnectionResetError,
            AttributeError,
            socket.timeout,
        ) as exc:
            logger.exception(f"Can't execute command {command} on host: {self.host}")
            self._reset_connection()
            raise HostIsNotAvailable(self.host) from exc

    def _read_channels(
        self,
        stdout: Channel,
        stderr: Channel,
        chunk_size: int = 4096,
    ) -> Tuple[str, str]:
        """Reads data from stdout/stderr channels.

        Reading channels is required before we wait for exit status of the remote process.
        Otherwise waiting step will hang indefinitely, see the warning from paramiko docs:
        # https://docs.paramiko.org/en/stable/api/channel.html#paramiko.channel.Channel.recv_exit_status

        Args:
            stdout: Channel of stdout stream of the remote process.
            stderr: Channel of stderr stream of the remote process.
            chunk_size: Max size of data chunk that we read from channel at a time.

        Returns:
            Tuple with stdout and stderr channels decoded into strings.
        """
        # We read data in chunks
        stdout_chunks = []
        stderr_chunks = []

        # Read from channels (if data is ready) until process exits
        while not stdout.exit_status_ready():
            if stdout.recv_ready():
                stdout_chunks.append(stdout.recv(chunk_size))
            if stderr.recv_stderr_ready():
                stderr_chunks.append(stderr.recv_stderr(chunk_size))

        # Wait for command to complete and flush its buffer before we read final output
        sleep(self.DELAY_AFTER_EXIT)

        # Read the remaining data from the channels:
        # If channel returns empty data chunk, it means that all data has been read
        while True:
            data_chunk = stdout.recv(chunk_size)
            if not data_chunk:
                break
            stdout_chunks.append(data_chunk)
        while True:
            data_chunk = stderr.recv_stderr(chunk_size)
            if not data_chunk:
                break
            stderr_chunks.append(data_chunk)

        # Combine chunks and decode results into regular strings
        full_stdout = b"".join(stdout_chunks)
        full_stderr = b"".join(stderr_chunks)

        return (full_stdout.decode(errors="ignore"), full_stderr.decode(errors="ignore"))

    def _create_connection(self, attempts: int = SSH_CONNECTION_ATTEMPTS) -> SSHClient:
        for attempt in range(attempts):
            connection = SSHClient()
            connection.set_missing_host_key_policy(AutoAddPolicy())
            try:
                if self.private_key_path:
                    logger.info(
                        f"Trying to connect to host {self.host} as {self.login} using SSH key "
                        f"{self.private_key_path} (attempt {attempt})"
                    )
                    connection.connect(
                        hostname=self.host,
                        port=self.port,
                        username=self.login,
                        pkey=_load_private_key(self.private_key_path, self.private_key_passphrase),
                        timeout=self.CONNECTION_TIMEOUT,
                    )
                else:
                    logger.info(
                        f"Trying to connect to host {self.host} as {self.login} using password "
                        f"(attempt {attempt})"
                    )
                    connection.connect(
                        hostname=self.host,
                        port=self.port,
                        username=self.login,
                        password=self.password,
                        timeout=self.CONNECTION_TIMEOUT,
                    )
                return connection
            except AuthenticationException:
                connection.close()
                logger.exception(f"Can't connect to host {self.host}")
                raise
            except (
                SSHException,
                ssh_exception.NoValidConnectionsError,
                AttributeError,
                socket.timeout,
                OSError,
            ) as exc:
                connection.close()
                can_retry = attempt + 1 < attempts
                if can_retry:
                    logger.warn(f"Can't connect to host {self.host}, will retry. Error: {exc}")
                    continue
                logger.exception(f"Can't connect to host {self.host}")
                raise HostIsNotAvailable(self.host) from exc

    def _reset_connection(self) -> None:
        if self.__connection:
            self.__connection.close()
        self.__connection = None
