from typing import Optional

from frostfs_testlib.cli.neogo.candidate import NeoGoCandidate
from frostfs_testlib.cli.neogo.contract import NeoGoContract
from frostfs_testlib.cli.neogo.db import NeoGoDb
from frostfs_testlib.cli.neogo.nep17 import NeoGoNep17
from frostfs_testlib.cli.neogo.node import NeoGoNode
from frostfs_testlib.cli.neogo.query import NeoGoQuery
from frostfs_testlib.cli.neogo.version import NeoGoVersion
from frostfs_testlib.cli.neogo.wallet import NeoGoWallet
from frostfs_testlib.shell import Shell


class NeoGo:
    candidate: Optional[NeoGoCandidate] = None
    contract: Optional[NeoGoContract] = None
    db: Optional[NeoGoDb] = None
    nep17: Optional[NeoGoNep17] = None
    node: Optional[NeoGoNode] = None
    query: Optional[NeoGoQuery] = None
    version: Optional[NeoGoVersion] = None
    wallet: Optional[NeoGoWallet] = None

    def __init__(
        self,
        shell: Shell,
        neo_go_exec_path: str,
        config_path: Optional[str] = None,
    ):
        self.candidate = NeoGoCandidate(shell, neo_go_exec_path, config_path=config_path)
        self.contract = NeoGoContract(shell, neo_go_exec_path, config_path=config_path)
        self.db = NeoGoDb(shell, neo_go_exec_path, config_path=config_path)
        self.nep17 = NeoGoNep17(shell, neo_go_exec_path, config_path=config_path)
        self.node = NeoGoNode(shell, neo_go_exec_path, config_path=config_path)
        self.query = NeoGoQuery(shell, neo_go_exec_path, config_path=config_path)
        self.version = NeoGoVersion(shell, neo_go_exec_path, config_path=config_path)
        self.wallet = NeoGoWallet(shell, neo_go_exec_path, config_path=config_path)
