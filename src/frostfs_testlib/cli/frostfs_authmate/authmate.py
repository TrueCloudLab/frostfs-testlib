from typing import Optional

from frostfs_testlib.cli.frostfs_authmate.secret import FrostfsAuthmateSecret
from frostfs_testlib.cli.frostfs_authmate.version import FrostfsAuthmateVersion
from frostfs_testlib.shell import Shell


class FrostfsAuthmate:
    secret: Optional[FrostfsAuthmateSecret] = None
    version: Optional[FrostfsAuthmateVersion] = None

    def __init__(self, shell: Shell, frostfs_authmate_exec_path: str):
        self.secret = FrostfsAuthmateSecret(shell, frostfs_authmate_exec_path)
        self.version = FrostfsAuthmateVersion(shell, frostfs_authmate_exec_path)
