from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class NeoGoWallet(CliCommand):
    def claim(
        self,
        address: str,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Claim GAS.

        Args:
            address: Address to claim GAS for.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG
        exec_param = {
            param: param_value for param, param_value in locals().items() if param not in ["self"]
        }
        exec_param["timeout"] = f"{timeout}s"
        return self._execute(
            "wallet claim",
            **exec_param,
        )

    def init(
        self,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        account: bool = False,
    ) -> CommandResult:
        """Create a new wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            account: Create a new account.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet init",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def convert(
        self,
        out: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Convert addresses from existing NEO2 NEP6-wallet to NEO3 format.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            out: Where to write converted wallet.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet convert",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def create(
        self,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Add an account to the existing wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet create",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def dump(
        self,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        decrypt: bool = False,
    ) -> CommandResult:
        """Check and dump an existing NEO wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            decrypt: Decrypt encrypted keys.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet dump",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def dump_keys(
        self,
        address: Optional[str] = None,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Check and dump an existing NEO wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            address: Address to print public keys for.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet dump-keys",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def export(
        self,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        decrypt: bool = False,
    ) -> CommandResult:
        """Export keys for address.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            decrypt: Decrypt encrypted keys.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet export",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def import_wif(
        self,
        wif: str,
        name: str,
        contract: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Import WIF of a standard signature contract.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            wif: WIF to import.
            name: Optional account name.
            contract: Verification script for custom contracts.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet import",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def import_multisig(
        self,
        wif: str,
        name: Optional[str] = None,
        min_number: int = 0,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Import multisig contract.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            wif: WIF to import.
            name: Optional account name.
            min_number: Minimal number of signatures (default: 0).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet import-multisig",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def import_deployed(
        self,
        wif: str,
        rpc_endpoint: str,
        name: Optional[str] = None,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        contract: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Import deployed contract.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            wif: WIF to import.
            name: Optional account name.
            contract: Contract hash or address.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG
        exec_param = {
            param: param_value for param, param_value in locals().items() if param not in ["self"]
        }
        exec_param["timeout"] = f"{timeout}s"
        return self._execute(
            "wallet import-deployed",
            **exec_param,
        )

    def remove(
        self,
        address: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        force: bool = False,
    ) -> CommandResult:
        """Remove an account from the wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            address: Account address or hash in LE form to be removed.
            force: Do not ask for a confirmation.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def sign(
        self,
        input_file: str,
        address: str,
        rpc_endpoint: Optional[str] = None,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        wallet_password: Optional[str] = None,
        out: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Cosign transaction with multisig/contract/additional account.

        Signs the given (in the input file) context (which must be a transaction signing context)
        for the given address using the given wallet. This command can output the resulting JSON
        (with additional signature added) right to the console (if no output file and no RPC
        endpoint specified) or into a file (which can be the same as input one). If an RPC endpoint
        is given it'll also try to construct a complete transaction and send it via RPC (printing
        its hash if everything is OK).

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            wallet_password: Wallet password.
            out: File to put JSON transaction to.
            input_file: File with JSON transaction.
            address: Address to use.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG
        exec_param = {
            param: param_value
            for param, param_value in locals().items()
            if param not in ["self", "wallet_password"]
        }
        exec_param["timeout"] = f"{timeout}s"
        if wallet_password is not None:
            return self._execute_with_password("wallet sign", wallet_password, **exec_param)

        if wallet_config:
            return self._execute("wallet sign", **exec_param)

        raise Exception(self.WALLET_PASSWD_ERROR_MSG)
