import base64
import json
import logging

import base58
from neo3.wallet import account as neo3_account
from neo3.wallet import wallet as neo3_wallet

logger = logging.getLogger("frostfs.testlib.utils")


def init_wallet(wallet_path: str, wallet_password: str):
    """
    Create new wallet and new account.
    Args:
        wallet_path:  The path to the wallet to save wallet.
        wallet_password: The password for new wallet.
    """
    wallet = neo3_wallet.Wallet()
    account = neo3_account.Account.create_new(wallet_password)
    wallet.account_add(account)
    with open(wallet_path, "w") as out:
        json.dump(wallet.to_json(), out)
    logger.info(f"Init new wallet: {wallet_path}, address: {account.address}")


def get_last_address_from_wallet(wallet_path: str, wallet_password: str):
    """
    Extracting the last address from the given wallet.
    Args:
        wallet_path:  The path to the wallet to extract address from.
        wallet_password: The password for the given wallet.
    Returns:
        The address for the wallet.
    """
    with open(wallet_path) as wallet_file:
        wallet = neo3_wallet.Wallet.from_json(json.load(wallet_file), password=wallet_password)
    address = wallet.accounts[-1].address
    logger.info(f"got address: {address}")
    return address


def get_wallet_public_key(wallet_path: str, wallet_password: str, format: str = "hex") -> str:
    def __fix_wallet_schema(wallet: dict) -> None:
        # Temporary function to fix wallets that do not conform to the schema
        # TODO: get rid of it once issue  is solved
        if "name" not in wallet:
            wallet["name"] = None
        for account in wallet["accounts"]:
            if "extra" not in account:
                account["extra"] = None

    #  Get public key from wallet file
    with open(wallet_path, "r") as file:
        wallet_content = json.load(file)
    __fix_wallet_schema(wallet_content)
    wallet_from_json = neo3_wallet.Wallet.from_json(wallet_content, password=wallet_password)
    public_key_hex = str(wallet_from_json.accounts[0].public_key)

    # Convert public key to specified format
    if format == "hex":
        return public_key_hex
    if format == "base58":
        public_key_base58 = base58.b58encode(bytes.fromhex(public_key_hex))
        return public_key_base58.decode("utf-8")
    if format == "base64":
        public_key_base64 = base64.b64encode(bytes.fromhex(public_key_hex))
        return public_key_base64.decode("utf-8")
    raise ValueError(f"Invalid public key format: {format}")


def load_wallet(path: str, passwd: str = "") -> neo3_wallet.Wallet:
    with open(path, "r") as wallet_file:
        wlt_data = wallet_file.read()
    return neo3_wallet.Wallet.from_json(json.loads(wlt_data), password=passwd)
