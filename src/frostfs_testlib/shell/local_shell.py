import logging
import subprocess
import tempfile
from datetime import datetime
from typing import IO, Optional

import pexpect

from frostfs_testlib.reporter import get_reporter
from frostfs_testlib.shell.interfaces import CommandInspector, CommandOptions, CommandResult, Shell

logger = logging.getLogger("frostfs.testlib.shell")
reporter = get_reporter()


class LocalShell(Shell):
    """Implements command shell on a local machine."""

    def __init__(self, command_inspectors: Optional[list[CommandInspector]] = None) -> None:
        super().__init__()
        self.command_inspectors = command_inspectors or []

    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        # If no options were provided, use default options
        options = options or CommandOptions()

        for inspector in self.command_inspectors:
            command = inspector.inspect(command)

        logger.info(f"Executing command: {command}")
        if options.interactive_inputs:
            return self._exec_interactive(command, options)
        return self._exec_non_interactive(command, options)

    def _exec_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        start_time = datetime.utcnow()
        log_file = tempfile.TemporaryFile()  # File is reliable cross-platform way to capture output

        try:
            command_process = pexpect.spawn(command, timeout=options.timeout)
        except (pexpect.ExceptionPexpect, OSError) as exc:
            raise RuntimeError(f"Command: {command}") from exc

        command_process.delaybeforesend = 1
        command_process.logfile_read = log_file

        try:
            for interactive_input in options.interactive_inputs:
                command_process.expect(interactive_input.prompt_pattern)
                command_process.sendline(interactive_input.input)
        except (pexpect.ExceptionPexpect, OSError) as exc:
            if options.check:
                raise RuntimeError(f"Command: {command}") from exc
        finally:
            result = self._get_pexpect_process_result(command_process)
            log_file.close()
            end_time = datetime.utcnow()
            self._report_command_result(command, start_time, end_time, result)

        if options.check and result.return_code != 0:
            raise RuntimeError(
                f"Command: {command}\nreturn code: {result.return_code}\n"
                f"Output: {result.stdout}"
            )
        return result

    def _exec_non_interactive(self, command: str, options: CommandOptions) -> CommandResult:
        start_time = datetime.utcnow()
        result = None

        try:
            command_process = subprocess.run(
                command,
                check=options.check,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=options.timeout,
                shell=True,
            )

            result = CommandResult(
                stdout=command_process.stdout or "",
                stderr="",
                return_code=command_process.returncode,
            )
        except subprocess.CalledProcessError as exc:
            # TODO: always set check flag to false and capture command result normally
            result = CommandResult(
                stdout=exc.stdout or "",
                stderr="",
                return_code=exc.returncode,
            )
            raise RuntimeError(
                f"Command: {command}\nError:\n"
                f"return code: {exc.returncode}\n"
                f"output: {exc.output}"
            ) from exc
        except OSError as exc:
            raise RuntimeError(f"Command: {command}\nOutput: {exc.strerror}") from exc
        finally:
            end_time = datetime.utcnow()
            self._report_command_result(command, start_time, end_time, result)
        return result

    def _get_pexpect_process_result(self, command_process: pexpect.spawn) -> CommandResult:
        """
        Captures output of the process.
        """
        # Wait for child process to end it's work
        if command_process.isalive():
            command_process.expect(pexpect.EOF)

        # Close the process to obtain the exit code
        command_process.close()
        return_code = command_process.exitstatus

        # Capture output from the log file
        log_file: IO[bytes] = command_process.logfile_read
        log_file.seek(0)
        output = log_file.read().decode()

        return CommandResult(stdout=output, stderr="", return_code=return_code)

    def _report_command_result(
        self,
        command: str,
        start_time: datetime,
        end_time: datetime,
        result: Optional[CommandResult],
    ) -> None:
        # TODO: increase logging level if return code is non 0, should be warning at least
        logger.info(
            f"Command: {command}\n"
            f"{'Success:' if result and result.return_code == 0 else 'Error:'}\n"
            f"return code: {result.return_code if result else ''} "
            f"\nOutput: {result.stdout if result else ''}"
        )

        if result:
            elapsed_time = end_time - start_time
            command_attachment = (
                f"COMMAND: {command}\n"
                f"RETCODE: {result.return_code}\n\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}\n"
                f"Start / End / Elapsed\t {start_time.time()} / {end_time.time()} / {elapsed_time}"
            )
            with reporter.step(f"COMMAND: {command}"):
                reporter.attach(command_attachment, "Command execution.txt")
