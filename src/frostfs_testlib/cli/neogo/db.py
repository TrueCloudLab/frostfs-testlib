from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.cli.neogo.network_type import NetworkType
from frostfs_testlib.shell import CommandResult


class NeoGoDb(CliCommand):
    def dump(
        self,
        config_path: str,
        out: str,
        network: NetworkType = NetworkType.PRIVATE,
        count: int = 0,
        start: int = 0,
    ) -> CommandResult:
        """Dump blocks (starting with block #1) to the file.

        Args:
            config_path: Path to config.
            network: Select network type (default: private).
            count: Number of blocks to be processed (default or 0: all chain) (default: 0).
            start: Block number to start from (default: 0) (default: 0).
            out: Output file (stdout if not given).

        Returns:
            Command's result.
        """
        return self._execute(
            "db dump",
            **{network.value: True},
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def restore(
        self,
        config_path: str,
        input_file: str,
        network: NetworkType = NetworkType.PRIVATE,
        count: int = 0,
        dump: Optional[str] = None,
        incremental: bool = False,
    ) -> CommandResult:
        """Dump blocks (starting with block #1) to the file.

        Args:
            config_path: Path to config.
            network: Select network type (default: private).
            count: Number of blocks to be processed (default or 0: all chain) (default: 0).
            input_file: Input file (stdin if not given).
            dump: Directory for storing JSON dumps.
            incremental: Use if dump is incremental.

        Returns:
            Command's result.
        """
        return self._execute(
            "db restore",
            **{network.value: True},
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
