from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsAdmMorphSubnet(CliCommand):
    def create(
        self, rpc_endpoint: str, address: str, wallet: str, notary: bool = False
    ) -> CommandResult:
        """Create FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            notary: Flag to create subnet in notary environment.
            rpc_endpoint: N3 RPC node endpoint.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet create",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def get(self, rpc_endpoint: str, subnet: str) -> CommandResult:
        """Read information about the FrostFS subnet.

        Args:
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet get",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def remove(
        self, rpc_endpoint: str, wallet: str, subnet: str, address: Optional[str] = None
    ) -> CommandResult:
        """Remove FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def admin_add(
        self,
        rpc_endpoint: str,
        wallet: str,
        admin: str,
        subnet: str,
        client: Optional[str] = None,
        group: Optional[str] = None,
        address: Optional[str] = None,
    ) -> CommandResult:
        """Add admin to the FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            admin: Hex-encoded public key of the admin.
            client: Add client admin instead of node one.
            group: Client group ID in text format (needed with --client only).
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet admin add",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def admin_remove(
        self,
        rpc_endpoint: str,
        wallet: str,
        admin: str,
        subnet: str,
        client: Optional[str] = None,
        address: Optional[str] = None,
    ) -> CommandResult:
        """Remove admin of the FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            admin: Hex-encoded public key of the admin.
            client: Remove client admin instead of node one.
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet admin remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def client_add(
        self,
        rpc_endpoint: str,
        wallet: str,
        subnet: str,
        client: Optional[str] = None,
        group: Optional[str] = None,
        address: Optional[str] = None,
    ) -> CommandResult:
        """Add client to the FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            client: Add client admin instead of node one.
            group: Client group ID in text format (needed with --client only).
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet client add",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def client_remove(
        self,
        rpc_endpoint: str,
        wallet: str,
        client: str,
        group: str,
        subnet: str,
        address: Optional[str] = None,
    ) -> CommandResult:
        """Remove client of the FrostFS subnet.

        Args:
            address: Address in the wallet, optional.
            client: Remove client admin instead of node one.
            group: ID of the client group to work with.
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet client remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def node_add(self, rpc_endpoint: str, wallet: str, node: str, subnet: str) -> CommandResult:
        """Add node to the FrostFS subnet.

        Args:
            node: Hex-encoded public key of the node.
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet node add",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def node_remove(self, rpc_endpoint: str, wallet: str, node: str, subnet: str) -> CommandResult:
        """Remove node from the FrostFS subnet.

        Args:
            node: Hex-encoded public key of the node.
            rpc_endpoint: N3 RPC node endpoint.
            subnet: ID of the subnet to read.
            wallet: Path to file with wallet.

        Returns:
            Command's result.
        """
        return self._execute(
            "morph subnet node remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
