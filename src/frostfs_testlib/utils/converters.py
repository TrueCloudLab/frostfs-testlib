import base64
import binascii
import json

import base58
from neo3.wallet import wallet as neo3_wallet


def str_to_ascii_hex(input: str) -> str:
    b = binascii.hexlify(input.encode())
    return str(b)[2:-1]


def ascii_hex_to_str(input: str) -> bytes:
    return bytes.fromhex(input)


# Two functions below do parsing of Base64-encoded byte arrays which
# tests receive from Neo node RPC calls.


def process_b64_bytearray_reverse(data: str) -> bytes:
    """
    This function decodes input data from base64, reverses the byte
    array and returns its string representation.
    """
    arr = bytearray(base64.standard_b64decode(data))
    arr.reverse()
    return binascii.b2a_hex(arr)


def process_b64_bytearray(data: str) -> bytes:
    """
    This function decodes input data from base64 and returns the
    bytearray string representation.
    """
    arr = bytearray(base64.standard_b64decode(data))
    return binascii.b2a_hex(arr)


def contract_hash_to_address(chash: str) -> str:
    """
    This function accepts contract hash in BE, then translates in to LE,
    prepends NEO wallet prefix and encodes to base58. It is equal to
    `UInt160ToString` method in NEO implementations.
    """
    be = bytearray(bytes.fromhex(chash))
    be.reverse()
    return base58.b58encode_check(b"\x35" + bytes(be)).decode()


def get_contract_hash_from_manifest(manifest_path: str) -> str:
    with open(manifest_path) as m:
        data = json.load(m)
        # cut off '0x' and return the hash
        return data["abi"]["hash"][2:]


def get_wif_from_private_key(priv_key: bytes) -> str:
    wif_version = b"\x80"
    compressed_flag = b"\x01"
    wif = base58.b58encode_check(wif_version + priv_key + compressed_flag)
    return wif.decode("utf-8")


def load_wallet(path: str, passwd: str = "") -> neo3_wallet.Wallet:
    with open(path, "r") as wallet_file:
        wlt_data = wallet_file.read()
    return neo3_wallet.Wallet.from_json(json.loads(wlt_data), password=passwd)
