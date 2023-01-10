from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliStorageGroup(CliCommand):
    def put(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        members: list[str],
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Put storage group to FrostFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            members: ID list of storage group members.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        members = ",".join(members)
        return self._execute(
            "storagegroup put",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def get(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        id: str,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Get storage group from FrostFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            id: Storage group identifier.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "storagegroup get",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def list(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        List storage groups in FrostFS container.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "storagegroup list",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def delete(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        id: str,
        raw: Optional[bool] = False,
        ttl: Optional[int] = None,
        bearer: Optional[str] = None,
        lifetime: Optional[int] = None,
        address: Optional[str] = None,
        xhdr: Optional[dict] = None,
    ) -> CommandResult:
        """
        Delete storage group from FrostFS.

        Args:
            address: Address of wallet account.
            bearer: File with signed JSON or binary encoded bearer token.
            cid: Container ID.
            id: Storage group identifier.
            raw: Set raw request option.
            lifetime: Storage group lifetime in epochs.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header.
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.

        Returns:
            Command's result.
        """
        return self._execute(
            "storagegroup delete",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
