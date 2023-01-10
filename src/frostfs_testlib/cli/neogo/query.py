from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class NeoGoQuery(CliCommand):
    def candidates(self, rpc_endpoint: str, timeout: str = "10s") -> CommandResult:
        """Get candidates and votes.

        Args:
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        return self._execute(
            "query candidates",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def committee(self, rpc_endpoint: str, timeout: str = "10s") -> CommandResult:
        """Get committee list.

        Args:
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        return self._execute(
            "query committee",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def height(self, rpc_endpoint: str, timeout: str = "10s") -> CommandResult:
        """Get node height.

        Args:
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        return self._execute(
            "query height",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def tx(self, tx_hash: str, rpc_endpoint: str, timeout: str = "10s") -> CommandResult:
        """Query transaction status.

        Args:
            tx_hash: Hash of transaction.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        return self._execute(
            f"query tx {tx_hash}",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self", "hash"]
            },
        )

    def voter(self, rpc_endpoint: str, timeout: str = "10s") -> CommandResult:
        """Print NEO holder account state.

        Args:
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        return self._execute(
            "query voter",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
