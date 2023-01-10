from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliContainer(CliCommand):
    def create(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        attributes: Optional[dict] = None,
        basic_acl: Optional[str] = None,
        await_mode: bool = False,
        disable_timestamp: bool = False,
        name: Optional[str] = None,
        nonce: Optional[str] = None,
        policy: Optional[str] = None,
        session: Optional[str] = None,
        subnet: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        Create a new container and register it in the FrostFS.
        It will be stored in the sidechain when the Inner Ring accepts it.

        Args:
            address: Address of wallet account.
            attributes: Comma separated pairs of container attributes in form of
                Key1=Value1,Key2=Value2.
            await_mode: Block execution until container is persisted.
            basic_acl: Hex encoded basic ACL value or keywords like 'public-read-write',
                'private', 'eacl-public-read' (default "private").
            disable_timestamp: Disable timestamp container attribute.
            name: Container name attribute.
            nonce: UUIDv4 nonce value for container.
            policy: QL-encoded or JSON-encoded placement policy or path to file with it.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            subnet: String representation of container subnetwork.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """
        return self._execute(
            "container create",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def delete(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        force: bool = False,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        Delete an existing container.
        Only the owner of the container has permission to remove the container.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            force: Do not check whether container contains locks and remove immediately.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """

        return self._execute(
            "container delete",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def get(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        to: Optional[str] = None,
        json_mode: bool = False,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        Get container field info.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            json_mode: Print or dump container in JSON format.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            to: Path to dump encoded container.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """
        return self._execute(
            "container get",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def get_eacl(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        to: Optional[str] = None,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        Get extended ACL table of container.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            to: Path to dump encoded container.
            session: Path to a JSON-encoded container session token.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.

        """
        return self._execute(
            "container get-eacl",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def list(
        self,
        rpc_endpoint: str,
        wallet: str,
        address: Optional[str] = None,
        owner: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
        **params,
    ) -> CommandResult:
        """
        List all created containers.

        Args:
            address: Address of wallet account.
            owner: Owner of containers (omit to use owner from private key).
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """
        return self._execute(
            "container list",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def list_objects(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        List existing objects in container.

        Args:
            address: Address of wallet account.
            cid: Container ID.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """
        return self._execute(
            "container list-objects",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )

    def set_eacl(
        self,
        rpc_endpoint: str,
        wallet: str,
        cid: str,
        address: Optional[str] = None,
        await_mode: bool = False,
        table: Optional[str] = None,
        session: Optional[str] = None,
        ttl: Optional[int] = None,
        xhdr: Optional[dict] = None,
        timeout: Optional[str] = None,
    ) -> CommandResult:
        """
        Set a new extended ACL table for the container.
        Container ID in the EACL table will be substituted with the ID from the CLI.

        Args:
            address: Address of wallet account.
            await_mode: Block execution until container is removed.
            cid: Container ID.
            rpc_endpoint: Remote node address (as 'multiaddr' or '<host>:<port>').
            session: Path to a JSON-encoded container session token.
            table: Path to file with JSON or binary encoded EACL table.
            ttl: TTL value in request meta header (default 2).
            wallet: WIF (NEP-2) string or path to the wallet or binary key.
            xhdr: Dict with request X-Headers.
            timeout: Timeout for the operation (default 15s).

        Returns:
            Command's result.
        """
        return self._execute(
            "container set-eacl",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
