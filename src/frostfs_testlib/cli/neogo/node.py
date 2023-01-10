from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.cli.neogo.network_type import NetworkType
from frostfs_testlib.shell import CommandResult


class NeoGoNode(CliCommand):
    def start(self, network: NetworkType = NetworkType.PRIVATE) -> CommandResult:
        """Start a NEO node.

        Args:
            network: Select network type (default: private).

        Returns:
            Command's result.
        """
        return self._execute("start", **{network.value: True})
