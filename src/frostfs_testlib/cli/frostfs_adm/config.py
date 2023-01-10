from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsAdmConfig(CliCommand):
    def init(self, path: str = "~/.frostfs/adm/config.yml") -> CommandResult:
        """Initialize basic frostfs-adm configuration file.

        Args:
            path: Path to config (default ~/.frostfs/adm/config.yml).

        Returns:
            Command's result.
        """
        return self._execute(
            "config init",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
