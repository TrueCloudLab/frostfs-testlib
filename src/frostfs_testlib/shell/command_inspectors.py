from frostfs_testlib.shell.interfaces import CommandInspector


class SudoInspector(CommandInspector):
    """Prepends command with sudo.

    If command is already prepended with sudo, then has no effect.
    """

    def inspect(self, command: str) -> str:
        if not command.startswith("sudo"):
            return f"sudo {command}"
        return command
