from typing import Optional

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsCliACL(CliCommand):
    def extended_create(
        self, cid: str, out: str, file: Optional[str] = None, rule: Optional[list] = None
    ) -> CommandResult:

        """Create extended ACL from the text representation.

        Rule consist of these blocks: <action> <operation> [<filter1> ...] [<target1> ...]
        Action is 'allow' or 'deny'.
        Operation is an object service verb: 'get', 'head', 'put', 'search', 'delete', 'getrange',
        or 'getrangehash'.

        Filter consists of <typ>:<key><match><value>
         Typ is 'obj' for object applied filter or 'req' for request applied filter.
          Key is a valid unicode string corresponding to object or request header key.
            Well-known system object headers start with '$Object:' prefix.
            User defined headers start without prefix.
            Read more about filter keys at:
                http://github.com/TrueCloudLab/frostfs-api/blob/master/proto-docs/acl.md#message-eaclrecordfilter
          Match is '=' for matching and '!=' for non-matching filter.
          Value is a valid unicode string corresponding to object or request header value.

        Target is
          'user' for container owner,
          'system' for Storage nodes in container and Inner Ring nodes,
          'others' for all other request senders,
          'pubkey:<key1>,<key2>,...' for exact request sender, where <key> is a hex-encoded 33-byte
          public key.

        When both '--rule' and '--file' arguments are used, '--rule' records will be placed higher
        in resulting extended ACL table.

        Args:
            cid: Container ID.
            file: Read list of extended ACL table records from from text file.
            out: Save JSON formatted extended ACL table in file.
            rule: Extended ACL table record to apply.

        Returns:
            Command's result.

        """
        return self._execute(
            "acl extended create",
            **{param: value for param, value in locals().items() if param not in ["self"]},
        )
