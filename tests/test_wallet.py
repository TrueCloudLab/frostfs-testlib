import json
import os
from unittest import TestCase
from uuid import uuid4

from neo3.wallet.wallet import Wallet

from frostfs_testlib.utils.wallet import init_wallet, get_last_address_from_wallet


class TestWallet(TestCase):
    DEFAULT_PASSWORD = "password"
    EMPTY_PASSWORD = ""

    def test_init_wallet(self):
        wallet_file_path = f"{str(uuid4())}.json"
        for password in (self.EMPTY_PASSWORD, self.DEFAULT_PASSWORD):
            wrong_password = "wrong_password"
            init_wallet(wallet_file_path, password)
            self.assertTrue(os.path.exists(wallet_file_path))
            with open(wallet_file_path, "r") as wallet_file:
                Wallet.from_json(json.load(wallet_file), password=password)
            with self.assertRaises(ValueError):
                with open(wallet_file_path, "r") as wallet_file:
                    Wallet.from_json(json.load(wallet_file), password=wrong_password)
            os.unlink(wallet_file_path)

    def test_get_last_address_from_wallet(self):
        wallet_file_path = f"{str(uuid4())}.json"
        init_wallet(wallet_file_path, self.DEFAULT_PASSWORD)
        with open(wallet_file_path, "r") as wallet_file:
            wallet = Wallet.from_json(json.load(wallet_file), password=self.DEFAULT_PASSWORD)
        last_address = wallet.accounts[-1].address
        self.assertEqual(
            get_last_address_from_wallet(wallet_file_path, self.DEFAULT_PASSWORD),
            last_address,
        )
        os.unlink(wallet_file_path)
