from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliSession(CliCommand):
    def create(
        self,
        rpc_endpoint: str,
        wallet: str,
        wallet_password: str,
        out: str,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        json: Optional[bool] = False,
    ) -> CommandResult:
        """
        Create session token.

        Args:
            address: Address of wallet account.
            out: File to write session token to.
            lifetime: Number of epochs for token to stay valid.
            json: Output token in JSON.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            wallet_password: Wallet password.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            "session create",
            wallet_password,
            **{
                param: value
                for param, value in locals().items()
                if param not in ["self", "wallet_password"]
            },
        )
