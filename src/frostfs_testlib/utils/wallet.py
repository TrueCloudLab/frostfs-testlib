import json
import logging

from neo3.wallet import wallet as neo3_wallet
from neo3.wallet import account as neo3_account

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
