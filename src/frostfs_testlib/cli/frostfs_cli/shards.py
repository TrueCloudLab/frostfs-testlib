from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliShards(CliCommand):
    def flush_cache(
        self,
        endpoint: str,
        wallet: str,
        wallet_password: str,
        id: Optional[list[str]],
        address: Optional[str] = None,
        all: bool = False,
    ) -> CommandResult:
        """
        Flush objects from the write-cache to the main storage.

        Args:
            address: Address of wallet account.
            id: List of shard IDs in base58 encoding.
            all: Process all shards.
            endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            wallet_password: Wallet password.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            f"control shards flush-cache",
            wallet_password,
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def set_mode(
        self,
        endpoint: str,
        wallet: str,
        wallet_password: str,
        mode: str,
        id: Optional[list[str]],
        address: Optional[str] = None,
        all: bool = False,
        clear_errors: bool = False,
    ) -> CommandResult:
        """
        Set work mode of the shard.

        Args:
            address: Address of wallet account.
            id: List of shard IDs in base58 encoding.
            mode: New shard mode ('degraded-read-only', 'read-only', 'read-write').
            all: Process all shards.
            clear_errors: Set shard error count to 0.
            endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            wallet_password: Wallet password.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            f"control shards set-mode",
            wallet_password,
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "wallet_password"]
            },
        )

    def dump(
        self,
        endpoint: str,
        wallet: str,
        wallet_password: str,
        id: str,
        path: str,
        address: Optional[str] = None,
        no_errors: bool = False,
    ) -> CommandResult:
        """
        Dump objects from shard to a file.

        Args:
            address: Address of wallet account.
            no_errors: Skip invalid/unreadable objects.
            id: Shard ID in base58 encoding.
            path: File to write objects to.
            endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            wallet_password: Wallet password.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            f"control shards dump",
            wallet_password,
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "wallet_password"]
            },
        )

    def list(
        self,
        endpoint: str,
        wallet: str,
        wallet_password: str,
        address: Optional[str] = None,
        json_mode: bool = False,
    ) -> CommandResult:
        """
        List shards of the storage node.

        Args:
            address: Address of wallet account.
            json_mode: Print shard info as a JSON array.
            endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            wallet_password: Wallet password.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            f"control shards list",
            wallet_password,
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "wallet_password"]
            },
        )
