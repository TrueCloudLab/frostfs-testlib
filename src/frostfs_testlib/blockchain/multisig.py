from frostfs_testlib.cli import NeoGo


class Multisig:
    def __init__(self, neogo: NeoGo, invoke_tx_file: str, block_period: int):
        self.neogo = neogo
        self.invoke_tx_file = invoke_tx_file
        self.block_period = block_period

    def create_and_send(
        self,
        contract_hash: str,
        contract_args: str,
        multisig_hash: str,
        wallets: list[str],
        passwords: list[str],
        address: str,
        endpoint: str,
    ) -> None:
        if not len(wallets):
            raise AttributeError("Got empty wallets list")

        self.neogo.contract.invokefunction(
            address=address,
            rpc_endpoint=endpoint,
            wallet=wallets[0],
            wallet_password=passwords[0],
            out=None if len(wallets) == 1 else self.invoke_tx_file,
            scripthash=contract_hash,
            arguments=contract_args,
            multisig_hash=multisig_hash,
        )

        if len(wallets) > 1:
            # sign with rest of wallets except the last one
            for wallet in wallets[1:-1]:
                self.neogo.wallet.sign(
                    wallet=wallet,
                    input_file=self.invoke_tx_file,
                    out=self.invoke_tx_file,
                    address=address,
                )

            # sign tx with last wallet and push it to blockchain
            self.neogo.wallet.sign(
                wallet=wallets[-1],
                input_file=self.invoke_tx_file,
                out=self.invoke_tx_file,
                address=address,
                rpc_endpoint=endpoint,
            )
