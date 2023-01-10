from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsAdmVersion(CliCommand):
    def get(self) -> CommandResult:
        """Application version

        Returns:
            Command's result.
        """
        return self._execute("", version=True)
