from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class NeoGoNep17(CliCommand):
    def balance(
        self,
        address: str,
        token: str,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Get address balance.

        Args:
            address: Address to use.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).
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
            "wallet nep17 balance",
            **exec_param,
        )

    def import_token(
        self,
        address: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        token: Optional[str] = None,
        rpc_endpoint: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Import NEP-17 token to a wallet.

        Args:
            address: Token contract address or hash in LE.
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).
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
            "wallet nep17 import",
            **exec_param,
        )

    def info(
        self,
        token: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
    ) -> CommandResult:
        """Print imported NEP-17 token info.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        return self._execute(
            "wallet nep17 info",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def remove(
        self,
        token: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        force: bool = False,
    ) -> CommandResult:
        """Remove NEP-17 token from the wallet.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).
            force: Do not ask for a confirmation.

        Returns:
            Command's result.
        """
        return self._execute(
            "wallet nep17 remove",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def transfer(
        self,
        token: str,
        to_address: str,
        rpc_endpoint: str,
        sysgas: Optional[float] = None,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        wallet_password: Optional[str] = None,
        out: Optional[str] = None,
        from_address: Optional[str] = None,
        force: bool = False,
        gas: Optional[float] = None,
        amount: float = 0,
        timeout: int = 10,
    ) -> CommandResult:
        """Transfers specified NEP-17 token amount.

        Transfer is executed with optional 'data' parameter and cosigners list attached to the
        transfer. See 'contract testinvokefunction' documentation for the details about 'data'
        parameter and cosigners syntax. If no 'data' is given then default nil value will be used.
        If no cosigners are given then the sender with CalledByEntry scope will be used as the only
        signer.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            wallet_password: Wallet password.
            out: File to put JSON transaction to.
            from_address: Address to send an asset from.
            to_address: Address to send an asset to.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).
            force: Do not ask for a confirmation.
            gas: Network fee to add to the transaction (prioritizing it).
            sysgas: System fee to add to transaction (compensating for execution).
            force: Do not ask for a confirmation.
            amount: Amount of asset to send.
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
            return self._execute_with_password(
                "wallet nep17 transfer",
                wallet_password,
                **exec_param,
            )
        if wallet_config:
            return self._execute(
                "wallet nep17 transfer",
                **exec_param,
            )

        raise Exception(self.WALLET_PASSWD_ERROR_MSG)

    def multitransfer(
        self,
        token: str,
        to_address: list[str],
        sysgas: float,
        rpc_endpoint: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        out: Optional[str] = None,
        from_address: Optional[str] = None,
        force: bool = False,
        gas: Optional[float] = None,
        amount: float = 0,
        timeout: int = 10,
    ) -> CommandResult:
        """Transfer NEP-17 tokens to multiple recipients.

        Args:
            wallet: Target location of the wallet file ('-' to read from stdin);
                conflicts with --wallet-config flag.
            wallet_config: Target location of the wallet config file; conflicts with --wallet flag.
            out: File to put JSON transaction to.
            from_address: Address to send an asset from.
            to_address: Address to send an asset to.
            token: Token to use (hash or name (for NEO/GAS or imported tokens)).
            force: Do not ask for a confirmation.
            gas: Network fee to add to the transaction (prioritizing it).
            sysgas: System fee to add to transaction (compensating for execution).
            force: Do not ask for a confirmation.
            amount: Amount of asset to send.
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
            "wallet nep17 multitransfer",
            **exec_param,
        )
