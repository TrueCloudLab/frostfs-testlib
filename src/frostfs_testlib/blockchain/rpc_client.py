import json
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger("frostfs.testlib.blockchain")


class NeoRPCException(Exception):
    pass


class RPCClient:
    def __init__(self, endpoint, timeout: int = 10):
        self.endpoint = endpoint
        self.timeout = timeout

    def get_raw_transaction(self, tx_hash):
        return self._call_endpoint("getrawtransaction", params=[tx_hash])

    def send_raw_transaction(self, raw_tx: str):
        return self._call_endpoint("sendrawtransaction", params=[raw_tx])

    def get_storage(self, sc_hash: str, storage_key: str):
        return self._call_endpoint("getstorage", params=[sc_hash, storage_key])

    def invoke_function(
        self,
        sc_hash: str,
        function: str,
        params: Optional[list] = None,
        signers: Optional[list] = None,
    ) -> Dict[str, Any]:
        return self._call_endpoint(
            "invokefunction", params=[sc_hash, function, params or [], signers or []]
        )

    def get_transaction_height(self, txid: str):
        return self._call_endpoint("gettransactionheight", params=[txid])

    def get_nep17_transfers(self, address, timestamps=None):
        params = [address]
        if timestamps:
            params.append(timestamps)
        return self._call_endpoint("getnep17transfers", params)

    def get_nep17_balances(self, address):
        return self._call_endpoint("getnep17balances", [address, 0])

    def get_application_log(self, tx_hash):
        return self._call_endpoint("getapplicationlog", params=[tx_hash])

    def get_contract_state(self, contract_id):
        """
        `contract_id` might be contract name, script hash or number
        """
        return self._call_endpoint("getcontractstate", params=[contract_id])

    def _call_endpoint(self, method, params=None) -> Dict[str, Any]:
        payload = _build_payload(method, params)
        logger.info(payload)
        try:
            response = requests.post(self.endpoint, data=payload, timeout=self.timeout)
            response.raise_for_status()
            if response.status_code == 200:
                if "result" in response.json():
                    return response.json()["result"]
            return response.json()
        except Exception as exc:
            raise NeoRPCException(
                f"Could not call method {method} "
                f"with endpoint: {self.endpoint}: {exc}"
                f"\nRequest sent: {payload}"
            ) from exc


def _build_payload(method, params: Optional[list] = None):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params or [], "id": 1})
    return payload.replace("'", '"')
