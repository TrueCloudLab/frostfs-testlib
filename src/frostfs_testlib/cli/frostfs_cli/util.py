from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliUtil(CliCommand):
    def sign_bearer_token(
            self,
            wallet: str,
            from_file: str,
            to_file: str,
            address: Optional[str] = None,
            json: Optional[bool] = False,
    ) -> CommandResult:
        """
        Sign bearer token to use it in requests.

        Args:
            address: Address of wallet account.
            from_file: File with JSON or binary encoded bearer token to sign.
            to_file: File to dump signed bearer token (default: binary encoded).
            json: Dump bearer token in JSON encoding.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.

        Returns:
            Command's result.
        """
        return self._execute(
            "util sign bearer-token",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def sign_session_token(
        self,
        wallet: str,
        from_file: str,
        to_file: str,
        address: Optional[str] = None,
    ) -> CommandResult:
        """
        Sign session token to use it in requests.

        Args:
            address: Address of wallet account.
            from_file: File with JSON encoded session token to sign.
            to_file: File to dump signed bearer token (default: binary encoded).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.

        Returns:
            Command's result.
        """
        return self._execute(
            "util sign session-token",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
