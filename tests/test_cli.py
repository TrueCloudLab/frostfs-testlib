from unittest import TestCase
from unittest.mock import Mock

from frostfs_testlib.cli import FrostfsAdm, FrostfsCli, NeoGo
from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell.interfaces import CommandOptions, InteractiveInput


class TestCli(TestCase):
    frostfs_adm_exec_path = "neo-adm-exec"
    frostfs_go_exec_path = "neo-go-exec"
    frostfs_cli_exec_path = "neo-cli-exec"

    address = "0x0000000000000000000"
    addresses = ["0x000000", "0xDEADBEEF", "0xBABECAFE"]
    amount = 100
    file1 = "file_1"
    file2 = "directory/file_2"
    manifest = "manifest1"
    token = "GAS"
    rpc_endpoint = "endpoint-1"
    sysgas: float = 0.001
    wallet = "wallet1"
    wallet_password = "P@$$w0rd"
    config_file = "config.yml"
    basic_acl = "1FBFBFFF"
    policy = "policy1"
    timeout = 20
    xhdr = {"param1": "value1", "param2": "value2"}

    def test_container_create(self):
        shell = Mock()
        frostfs_cli = FrostfsCli(
            config_file=self.config_file,
            frostfs_cli_exec_path=self.frostfs_cli_exec_path,
            shell=shell,
        )
        frostfs_cli.container.create(
            rpc_endpoint=self.rpc_endpoint,
            wallet=self.wallet,
            basic_acl=self.basic_acl,
            policy=self.policy,
            await_mode=True,
            xhdr=self.xhdr,
        )

        xhdr = ",".join(f"{param}={value}" for param, value in self.xhdr.items())
        expected_command = (
            f"{self.frostfs_cli_exec_path} --config {self.config_file} container create "
            f"--rpc-endpoint '{self.rpc_endpoint}' --wallet '{self.wallet}' "
            f"--basic-acl '{self.basic_acl}' --await --policy '{self.policy}' "
            f"--xhdr '{xhdr}'"
        )

        shell.exec.assert_called_once_with(expected_command)

    def test_bad_wallet_argument(self):
        shell = Mock()
        neo_go = NeoGo(
            shell=shell, config_path=self.config_file, neo_go_exec_path=self.frostfs_go_exec_path
        )
        with self.assertRaises(Exception) as exc_msg:
            neo_go.contract.add_group(
                address=self.address,
                manifest=self.manifest,
                wallet_password=self.wallet_password,
            )
        self.assertEqual(CliCommand.WALLET_SOURCE_ERROR_MSG, str(exc_msg.exception))

        with self.assertRaises(Exception) as exc_msg:
            neo_go.contract.add_group(
                wallet=self.wallet,
                wallet_password=self.wallet_password,
                wallet_config=self.config_file,
                address=self.address,
                manifest=self.manifest,
            )
        self.assertEqual(CliCommand.WALLET_SOURCE_ERROR_MSG, str(exc_msg.exception))

        with self.assertRaises(Exception) as exc_msg:
            neo_go.contract.add_group(
                wallet=self.wallet,
                address=self.address,
                manifest=self.manifest,
            )
        self.assertEqual(CliCommand.WALLET_PASSWD_ERROR_MSG, str(exc_msg.exception))

    def test_wallet_sign(self):
        shell = Mock()
        neo_go = NeoGo(
            shell=shell, config_path=self.config_file, neo_go_exec_path=self.frostfs_go_exec_path
        )
        neo_go.wallet.sign(
            input_file=self.file1,
            out=self.file2,
            rpc_endpoint=self.rpc_endpoint,
            address=self.address,
            wallet=self.wallet,
            wallet_password=self.wallet_password,
            timeout=self.timeout,
        )

        expected_command = (
            f"{self.frostfs_go_exec_path} --config_path {self.config_file} wallet sign "
            f"--input-file '{self.file1}' --address '{self.address}' "
            f"--rpc-endpoint '{self.rpc_endpoint}' --wallet '{self.wallet}' "
            f"--out '{self.file2}' --timeout '{self.timeout}s'"
        )

        shell.exec.assert_called_once_with(
            expected_command,
            options=CommandOptions(
                interactive_inputs=[
                    InteractiveInput(prompt_pattern="assword", input=self.wallet_password)
                ]
            ),
        )

    def test_subnet_create(self):
        shell = Mock()
        frostfs_adm = FrostfsAdm(
            config_file=self.config_file,
            frostfs_adm_exec_path=self.frostfs_adm_exec_path,
            shell=shell,
        )
        frostfs_adm.subnet.create(
            address=self.address,
            rpc_endpoint=self.rpc_endpoint,
            wallet=self.wallet,
            notary=True,
        )

        expected_command = (
            f"{self.frostfs_adm_exec_path} --config {self.config_file} morph subnet create "
            f"--rpc-endpoint '{self.rpc_endpoint}' --address '{self.address}' "
            f"--wallet '{self.wallet}' --notary"
        )

        shell.exec.assert_called_once_with(expected_command)

    def test_wallet_nep17_multitransfer(self):
        shell = Mock()
        neo_go = NeoGo(
            shell=shell, config_path=self.config_file, neo_go_exec_path=self.frostfs_go_exec_path
        )
        neo_go.nep17.multitransfer(
            wallet=self.wallet,
            token=self.token,
            to_address=self.addresses,
            sysgas=self.sysgas,
            rpc_endpoint=self.rpc_endpoint,
            amount=self.amount,
            force=True,
            from_address=self.address,
            timeout=self.timeout,
        )

        to_address = "".join(f" --to '{address}'" for address in self.addresses)
        expected_command = (
            f"{self.frostfs_go_exec_path} --config_path {self.config_file} "
            f"wallet nep17 multitransfer --token '{self.token}'"
            f"{to_address} --sysgas '{self.sysgas}' --rpc-endpoint '{self.rpc_endpoint}' "
            f"--wallet '{self.wallet}' --from '{self.address}' --force --amount {self.amount} "
            f"--timeout '{self.timeout}s'"
        )

        shell.exec.assert_called_once_with(expected_command)

    def test_version(self):
        shell = Mock()
        frostfs_adm = FrostfsAdm(shell=shell, frostfs_adm_exec_path=self.frostfs_adm_exec_path)
        frostfs_adm.version.get()

        shell.exec.assert_called_once_with(f"{self.frostfs_adm_exec_path}   --version")
