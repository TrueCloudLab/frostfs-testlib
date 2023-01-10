from typing import Optional

from frostfs_testlib.cli.frostfs_cli.accounting import FrostfsCliAccounting
from frostfs_testlib.cli.frostfs_cli.acl import FrostfsCliACL
from frostfs_testlib.cli.frostfs_cli.container import FrostfsCliContainer
from frostfs_testlib.cli.frostfs_cli.netmap import FrostfsCliNetmap
from frostfs_testlib.cli.frostfs_cli.object import FrostfsCliObject
from frostfs_testlib.cli.frostfs_cli.session import FrostfsCliSession
from frostfs_testlib.cli.frostfs_cli.shards import FrostfsCliShards
from frostfs_testlib.cli.frostfs_cli.storagegroup import FrostfsCliStorageGroup
from frostfs_testlib.cli.frostfs_cli.util import FrostfsCliUtil
from frostfs_testlib.cli.frostfs_cli.version import FrostfsCliVersion
from frostfs_testlib.shell import Shell


class FrostfsCli:
    accounting: Optional[FrostfsCliAccounting] = None
    acl: Optional[FrostfsCliACL] = None
    container: Optional[FrostfsCliContainer] = None
    netmap: Optional[FrostfsCliNetmap] = None
    object: Optional[FrostfsCliObject] = None
    session: Optional[FrostfsCliSession] = None
    shards: Optional[FrostfsCliShards] = None
    storagegroup: Optional[FrostfsCliStorageGroup] = None
    util: Optional[FrostfsCliUtil] = None
    version: Optional[FrostfsCliVersion] = None

    def __init__(self, shell: Shell, frostfs_cli_exec_path: str, config_file: Optional[str] = None):
        self.accounting = FrostfsCliAccounting(shell, frostfs_cli_exec_path, config=config_file)
        self.acl = FrostfsCliACL(shell, frostfs_cli_exec_path, config=config_file)
        self.container = FrostfsCliContainer(shell, frostfs_cli_exec_path, config=config_file)
        self.netmap = FrostfsCliNetmap(shell, frostfs_cli_exec_path, config=config_file)
        self.object = FrostfsCliObject(shell, frostfs_cli_exec_path, config=config_file)
        self.session = FrostfsCliSession(shell, frostfs_cli_exec_path, config=config_file)
        self.shards = FrostfsCliShards(shell, frostfs_cli_exec_path, config=config_file)
        self.storagegroup = FrostfsCliStorageGroup(shell, frostfs_cli_exec_path, config=config_file)
        self.util = FrostfsCliUtil(shell, frostfs_cli_exec_path, config=config_file)
        self.version = FrostfsCliVersion(shell, frostfs_cli_exec_path, config=config_file)
