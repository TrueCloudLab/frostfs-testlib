from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class NeoGoContract(CliCommand):
    def compile(
        self,
        input_file: str,
        out: str,
        manifest: str,
        config: str,
        no_standards: bool = False,
        no_events: bool = False,
        no_permissions: bool = False,
        bindings: Optional[str] = None,
    ) -> CommandResult:
        """Compile a smart contract to a .nef file.

        Args:
            input_file: Input file for the smart contract to be compiled.
            out: Output of the compiled contract.
            manifest: Emit contract manifest (*.manifest.json) file into separate file using
                configuration input file (*.yml).
            config: Configuration input file (*.yml).
            no_standards: Do not check compliance with supported standards.
            no_events: Do not check emitted events with the manifest.
            no_permissions: Do not check if invoked contracts are allowed in manifest.
            bindings: Output file for smart-contract bindings configuration.

        Returns:
            Command's result.
        """
        return self._execute(
            "contract compile",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def deploy(
        self,
        address: str,
        input_file: str,
        manifest: str,
        rpc_endpoint: str,
        sysgas: Optional[float] = None,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        wallet_password: Optional[str] = None,
        gas: Optional[float] = None,
        out: Optional[str] = None,
        force: bool = False,
        timeout: int = 10,
    ) -> CommandResult:
        """Deploy a smart contract (.nef with description)

        Args:
            wallet: Wallet to use to get the key for transaction signing;
                conflicts with wallet_config.
            wallet_config: Path to wallet config to use to get the key for transaction signing;
                conflicts with wallet.
            wallet_password: Wallet password.
            address: Address to use as transaction signee (and gas source).
            gas: Network fee to add to the transaction (prioritizing it).
            sysgas: System fee to add to transaction (compensating for execution).
            out: File to put JSON transaction to.
            force: Do not ask for a confirmation.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).
            input_file: Input file for the smart contract (*.nef).
            manifest: Emit contract manifest (*.manifest.json) file into separate file using
                configuration input file (*.yml).

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
                "contract deploy",
                wallet_password,
                **exec_param,
            )
        if wallet_config:
            return self._execute(
                "contract deploy",
                **exec_param,
            )

        raise Exception(self.WALLET_PASSWD_ERROR_MSG)

    def generate_wrapper(
        self,
        out: str,
        hash: str,
        config: Optional[str] = None,
        manifest: Optional[str] = None,
    ) -> CommandResult:
        """Generate wrapper to use in other contracts.

        Args:
            config: Configuration file to use.
            manifest: Read contract manifest (*.manifest.json) file.
            out: Output of the compiled contract.
            hash: Smart-contract hash.

        Returns:
            Command's result.
        """
        return self._execute(
            "contract generate-wrapper",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def invokefunction(
        self,
        scripthash: str,
        address: Optional[str] = None,
        wallet: Optional[str] = None,
        method: Optional[str] = None,
        arguments: Optional[str] = None,
        multisig_hash: Optional[str] = None,
        wallet_config: Optional[str] = None,
        wallet_password: Optional[str] = None,
        gas: Optional[float] = None,
        sysgas: Optional[float] = None,
        out: Optional[str] = None,
        force: bool = False,
        rpc_endpoint: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Executes given (as a script hash) deployed script.

        Script is executed with the given method, arguments and signers. Sender is included in
        the list of signers by default with None witness scope. If you'd like to change default
        sender's scope, specify it via signers parameter. See testinvokefunction documentation
        for the details about parameters. It differs from testinvokefunction in that this command
        sends an invocation transaction to the network.

        Args:
            scripthash: Function hash.
            method: Call method.
            arguments: Method arguments.
            multisig_hash: Multisig hash.
            wallet: Wallet to use to get the key for transaction signing;
                conflicts with wallet_config.
            wallet_config: Path to wallet config to use to get the key for transaction signing;
                conflicts with wallet.
            wallet_password: Wallet password.
            address: Address to use as transaction signee (and gas source).
            gas: Network fee to add to the transaction (prioritizing it).
            sysgas: System fee to add to transaction (compensating for execution).
            out: File to put JSON transaction to.
            force: Force-push the transaction in case of bad VM state after test script invocation.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """

        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG

        multisig_hash = f"-- {multisig_hash}" or ""
        post_data = f"{scripthash} {method or ''} {arguments or ''} {multisig_hash}"
        exec_param = {
            param: param_value
            for param, param_value in locals().items()
            if param
            not in [
                "self",
                "scripthash",
                "method",
                "arguments",
                "multisig_hash",
                "wallet_password",
            ]
        }
        exec_param["timeout"] = f"{timeout}s"
        exec_param["post_data"] = post_data
        if wallet_password is not None:
            return self._execute_with_password(
                "contract invokefunction", wallet_password, **exec_param
            )
        if wallet_config:
            return self._execute("contract invokefunction", **exec_param)

        raise Exception(self.WALLET_PASSWD_ERROR_MSG)

    def testinvokefunction(
        self,
        scripthash: str,
        wallet: Optional[str] = None,
        wallet_password: Optional[str] = None,
        method: Optional[str] = None,
        arguments: Optional[str] = None,
        multisig_hash: Optional[str] = None,
        rpc_endpoint: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Executes given (as a script hash) deployed script.

        Script is executed with the given method, arguments and signers (sender is not included
        by default). If no method is given "" is passed to the script, if no arguments are given,
        an empty array is passed, if no signers are given no array is passed. If signers are
        specified, the first one of them is treated as a sender. All of the given arguments are
        encapsulated into array before invoking the script. The script thus should follow the
        regular convention of smart contract arguments (method string and an array of other
        arguments).
        See more information and samples in `neo-go contract testinvokefunction --help`.

        Args:
            scripthash: Function hash.
            wallet: Wallet to use for testinvoke.
            wallet_password: Wallet password.
            method: Call method.
            arguments: Method arguments.
            multisig_hash: Multisig hash.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        multisig_hash = f"-- {multisig_hash}" if multisig_hash else ""
        post_data = f"{scripthash} {method or ''} {arguments or ''} {multisig_hash}"
        exec_param = {
            param: param_value
            for param, param_value in locals().items()
            if param
            not in [
                "self",
                "scripthash",
                "method",
                "arguments",
                "multisig_hash",
                "wallet_password",
            ]
        }
        exec_param["timeout"] = f"{timeout}s"
        exec_param["post_data"] = post_data
        if wallet_password is not None:
            return self._execute_with_password(
                "contract testinvokefunction", wallet_password, **exec_param
            )

        return self._execute("contract testinvokefunction", **exec_param)

    def testinvokescript(
        self,
        input_file: str,
        rpc_endpoint: Optional[str] = None,
        timeout: int = 10,
    ) -> CommandResult:
        """Executes given compiled AVM instructions in NEF format.

        Instructions are executed with the given set of signers not including sender by default.
        See testinvokefunction documentation for the details about parameters.

        Args:
            input_file: Input location of the .nef file that needs to be invoked.
            rpc_endpoint: RPC node address.
            timeout: Timeout for the operation (default: 10s).

        Returns:
            Command's result.
        """
        exec_param = {
            param: param_value for param, param_value in locals().items() if param not in ["self"]
        }
        exec_param["timeout"] = f"{timeout}s"
        return self._execute(
            "contract testinvokescript",
            **exec_param,
        )

    def init(self, name: str, skip_details: bool = False) -> CommandResult:
        """Initialize a new smart-contract in a directory with boiler plate code.

        Args:
            name: Name of the smart-contract to be initialized.
            skip_details: Skip filling in the projects and contract details.

        Returns:
            Command's result.
        """
        return self._execute(
            "contract init",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def inspect(
        self,
        input_file: Optional[str] = None,
        compile: Optional[str] = None,
    ) -> CommandResult:
        """Creates a user readable dump of the program instructions.

        Args:
            input_file: Input file of the program (either .go or .nef).
            compile: Compile input file (it should be go code then).

        Returns:
            Command's result.
        """
        return self._execute(
            "contract inspect",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def calc_hash(
        self,
        input_file: str,
        manifest: str,
        sender: Optional[str] = None,
    ) -> CommandResult:
        """Calculates hash of a contract after deployment.

        Args:
            input_file: Path to NEF file.
            sender: Sender script hash or address.
            manifest: Path to manifest file.

        Returns:
            Command's result.
        """
        return self._execute(
            "contract calc-hash",
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def add_group(
        self,
        manifest: str,
        address: str,
        wallet: Optional[str] = None,
        wallet_config: Optional[str] = None,
        wallet_password: Optional[str] = None,
        sender: Optional[str] = None,
        nef: Optional[str] = None,
    ) -> CommandResult:
        """Adds group to the manifest.

        Args:
            wallet: Wallet to use to get the key for transaction signing;
                conflicts with wallet_config.
            wallet_config: Path to wallet config to use to get the key for transaction signing;
                conflicts with wallet.
            wallet_password: Wallet password.
            sender: Deploy transaction sender.
            address: Account to sign group with.
            nef: Path to the NEF file.
            manifest: Path to the manifest.

        Returns:
            Command's result.
        """
        assert bool(wallet) ^ bool(wallet_config), self.WALLET_SOURCE_ERROR_MSG
        exec_param = {
            param: param_value
            for param, param_value in locals().items()
            if param not in ["self", "wallet_password"]
        }
        if wallet_password is not None:
            return self._execute_with_password(
                "contract manifest add-group", wallet_password, **exec_param
            )
        if wallet_config:
            return self._execute("contract manifest add-group", **exec_param)

        raise Exception(self.WALLET_PASSWD_ERROR_MSG)
