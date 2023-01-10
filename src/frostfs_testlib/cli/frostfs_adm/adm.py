from typing import Optional

from frostfs_testlib.cli.frostfs_adm.config import FrostfsAdmConfig
from frostfs_testlib.cli.frostfs_adm.morph import FrostfsAdmMorph
from frostfs_testlib.cli.frostfs_adm.storage_config import FrostfsAdmStorageConfig
from frostfs_testlib.cli.frostfs_adm.subnet import FrostfsAdmMorphSubnet
from frostfs_testlib.cli.frostfs_adm.version import FrostfsAdmVersion
from frostfs_testlib.shell import Shell


class FrostfsAdm:
    morph: Optional[FrostfsAdmMorph] = None
    subnet: Optional[FrostfsAdmMorphSubnet] = None
    storage_config: Optional[FrostfsAdmStorageConfig] = None
    version: Optional[FrostfsAdmVersion] = None

    def __init__(self, shell: Shell, frostfs_adm_exec_path: str, config_file: Optional[str] = None):
        self.config = FrostfsAdmConfig(shell, frostfs_adm_exec_path, config=config_file)
        self.morph = FrostfsAdmMorph(shell, frostfs_adm_exec_path, config=config_file)
        self.subnet = FrostfsAdmMorphSubnet(shell, frostfs_adm_exec_path, config=config_file)
        self.storage_config = FrostfsAdmStorageConfig(shell, frostfs_adm_exec_path, config=config_file)
        self.version = FrostfsAdmVersion(shell, frostfs_adm_exec_path, config=config_file)
