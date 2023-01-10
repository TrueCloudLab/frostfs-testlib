from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliNetmap(CliCommand):
    def epoch(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        generate_key: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Get current epoch number.

        Args:
            address: Address of wallet account.
            generate_key: Generate new private key.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: Path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "netmap epoch",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def netinfo(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        generate_key: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Get information about FrostFS network.

        Args:
            address: Address of wallet account
            generate_key: Generate new private key
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>')
            ttl: TTL value in request meta header (default 2)
            wallet: Path to the wallet or binary key
            xhdr: Request X-Headers in form of Key=Value

        Returns:
            Command's result.
        """
        return self._execute(
            "netmap netinfo",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def nodeinfo(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        generate_key: bool = False,
        json: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Get target node info.

        Args:
            address: Address of wallet account.
            generate_key: Generate new private key.
            json: Print node info in JSON format.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: Path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "netmap nodeinfo",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def snapshot(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        generate_key: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Request current local snapshot of the network map.

        Args:
            address: Address of wallet account.
            generate_key: Generate new private key.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: Path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "netmap snapshot",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
