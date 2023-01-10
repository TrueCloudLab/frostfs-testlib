import json
from time import sleep
from typing import Optional

from cli import NeoGo
from shell import Shell
from utils.converters import process_b64_bytearray

from frostfs_testlib.blockchain import Multisig


class RoleDesignation:
    def __init__(
        self,
        shell: Shell,
        neo_go_exec_path: str,
        block_period: int,
        designate_contract: str,
    ):
        self.neogo = NeoGo(shell, neo_go_exec_path)
        self.block_period = block_period
        self.designate_contract = designate_contract

    def set_notary_nodes(
        self,
        addr: str,
        pubkeys: list[str],
        script_hash: str,
        wallet: str,
        passwd: str,
        endpoint: str,
    ) -> str:
        keys = [f"bytes:{k}" for k in pubkeys]
        keys_str = " ".join(keys)
        out = self.neogo.contract.invokefunction(
            address=addr,
            scripthash=self.designate_contract,
            wallet=wallet,
            wallet_password=passwd,
            rpc_endpoint=endpoint,
            arguments=f"designateAsRole int:32 [ {keys_str} ]  -- {script_hash}",
            force=True,
        )
        sleep(self.block_period)
        return out.stdout.split(" ")[-1]

    def set_inner_ring(
        self,
        addr: str,
        pubkeys: list[str],
        script_hash: str,
        wallet: str,
        passwd: str,
        endpoint: str,
    ) -> str:
        keys = [f"bytes:{k}" for k in pubkeys]
        keys_str = " ".join(keys)
        out = self.neogo.contract.invokefunction(
            address=addr,
            scripthash=self.designate_contract,
            wallet=wallet,
            wallet_password=passwd,
            rpc_endpoint=endpoint,
            arguments=f"designateAsRole int:16 [ {keys_str} ]  -- {script_hash}",
            force=True,
        )
        sleep(self.block_period)
        return out.stdout.split(" ")[-1]

    def set_oracles(
        self,
        addr: str,
        pubkeys: list[str],
        script_hash: str,
        wallet: str,
        passwd: str,
        endpoint: str,
    ) -> str:
        keys = [f"bytes:{k}" for k in pubkeys]
        keys_str = " ".join(keys)
        out = self.neogo.contract.invokefunction(
            address=addr,
            scripthash=self.designate_contract,
            wallet=wallet,
            wallet_password=passwd,
            rpc_endpoint=endpoint,
            arguments=f"designateAsRole int:8 [ {keys_str} ]  -- {script_hash}",
            force=True,
        )
        sleep(self.block_period)
        return out.stdout.split(" ")[-1]

    def set_notary_nodes_multisig_tx(
        self,
        pubkeys: list[str],
        script_hash: str,
        wallets: list[str],
        passwords: list[str],
        address: str,
        endpoint: str,
        invoke_tx_file: str,
    ) -> None:
        keys = [f"bytes:{k}" for k in pubkeys]
        keys_str = " ".join(keys)
        multisig = Multisig(
            self.neogo, invoke_tx_file=invoke_tx_file, block_period=self.block_period
        )
        multisig.create_and_send(
            self.designate_contract,
            f"designateAsRole int:32 [ {keys_str} ]",
            script_hash,
            wallets,
            passwords,
            address,
            endpoint,
        )
        sleep(self.block_period)

    def set_inner_ring_multisig_tx(
        self,
        pubkeys: list[str],
        script_hash: str,
        wallets: list[str],
        passwords: list[str],
        address: str,
        endpoint: str,
        invoke_tx_file: str,
    ) -> None:
        keys = [f"bytes:{k}" for k in pubkeys]
        keys_str = " ".join(keys)
        multisig = Multisig(
            self.neogo, invoke_tx_file=invoke_tx_file, block_period=self.block_period
        )
        multisig.create_and_send(
            self.designate_contract,
            f"designateAsRole int:16 [ {keys_str} ]",
            script_hash,
            wallets,
            passwords,
            address,
            endpoint,
        )
        sleep(self.block_period)

    def check_candidates(self, contract_hash: str, endpoint: str) -> Optional[list[str]]:
        out = self.neogo.contract.testinvokefunction(
            scripthash=contract_hash,
            method="innerRingCandidates",
            rpc_endpoint=endpoint,
        )
        output_dict = json.loads(out.stdout.replace("\n", ""))
        candidates = output_dict["stack"][0]["value"]
        if len(candidates) == 0:
            return None
        # TODO: return a list of keys
        return [process_b64_bytearray(candidate["value"][0]["value"]) for candidate in candidates]
