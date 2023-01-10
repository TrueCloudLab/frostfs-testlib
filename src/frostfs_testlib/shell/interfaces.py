from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from neofs_testlib.defaults import Options


@dataclass
class InteractiveInput:
    """Interactive input for a shell command.

    Attributes:
        prompt_pattern: Regular expression that defines expected prompt from the command.
        input: User input that should be supplied to the command in response to the prompt.
    """

    prompt_pattern: str
    input: str


class CommandInspector(ABC):
    """Interface of inspector that processes command text before execution."""

    @abstractmethod
    def inspect(self, command: str) -> str:
        """Transforms command text and returns modified command.

        Args:
            command: Command to transform with this inspector.

        Returns:
            Transformed command text.
        """


@dataclass
class CommandOptions:
    """Options that control command execution.

    Attributes:
        interactive_inputs: User inputs that should be interactively supplied to
            the command during execution.
        close_stdin: Controls whether stdin stream should be closed after feeding interactive
            inputs or after requesting non-interactive command. If shell implementation does not
            support this functionality, it should ignore this flag without raising an error.
        timeout: Timeout for command execution (in seconds).
        check: Controls whether to check return code of the command. Set to False to
            ignore non-zero return codes.
        no_log: Do not print output to logger if True.
    """

    interactive_inputs: Optional[list[InteractiveInput]] = None
    close_stdin: bool = False
    timeout: Optional[int] = None
    check: bool = True
    no_log: bool = False

    def __post_init__(self):
        if self.timeout is None:
            self.timeout = Options.get_default_shell_timeout()


@dataclass
class CommandResult:
    """Represents a result of a command executed via shell.

    Attributes:
        stdout: Complete content of stdout stream.
        stderr: Complete content of stderr stream.
        return_code: Return code (or exit code) of the command's process.
    """

    stdout: str
    stderr: str
    return_code: int


class Shell(ABC):
    """Interface of a command shell on some system (local or remote)."""

    @abstractmethod
    def exec(self, command: str, options: Optional[CommandOptions] = None) -> CommandResult:
        """Executes specified command on this shell.

        To execute interactive command, user inputs should be specified in *options*.

        Args:
            command: Command to execute on the shell.
            options: Options that control command execution.

        Returns:
            Command's result.
        """
