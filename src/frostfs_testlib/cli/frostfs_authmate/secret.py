from typing import Optional, Union

from frostfs_testlib.cli.cli_command import CliCommand
from frostfs_testlib.shell import CommandResult


class FrostfsAuthmateSecret(CliCommand):
    def obtain(
        self,
        wallet: str,
        wallet_password: str,
        peer: str,
        gate_wallet: str,
        access_key_id: str,
        address: Optional[str] = None,
        gate_address: Optional[str] = None,
    ) -> CommandResult:
        """Obtain a secret from FrostFS network.

        Args:
            wallet: Path to the wallet.
            wallet_password: Wallet password.
            address: Address of wallet account.
            peer: Address of frostfs peer to connect to.
            gate_wallet: Path to the wallet.
            gate_address: Address of wallet account.
            access_key_id: Access key id for s3.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            "obtain-secret",
            wallet_password,
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )

    def issue(
        self,
        wallet: str,
        wallet_password: str,
        peer: str,
        bearer_rules: str,
        gate_public_key: Union[str, list[str]],
        address: Optional[str] = None,
        container_id: Optional[str] = None,
        container_friendly_name: Optional[str] = None,
        container_placement_policy: Optional[str] = None,
        session_tokens: Optional[str] = None,
        lifetime: Optional[str] = None,
        container_policy: Optional[str] = None,
        aws_cli_credentials: Optional[str] = None,
    ) -> CommandResult:
        """Obtain a secret from FrostFS network

        Args:
            wallet: Path to the wallet.
            wallet_password: Wallet password.
            address: Address of wallet account.
            peer: Address of a frostfs peer to connect to.
            bearer_rules: Rules for bearer token as plain json string.
            gate_public_key: Public 256r1 key of a gate (send list[str] of keys to use multiple gates).
            container_id: Auth container id to put the secret into.
            container_friendly_name: Friendly name of auth container to put the secret into.
            container_placement_policy: Placement policy of auth container to put the secret into
                (default: "REP 2 IN X CBF 3 SELECT 2 FROM * AS X").
            session_tokens: Create session tokens with rules, if the rules are set as 'none', no
                session tokens will be created.
            lifetime: Lifetime of tokens. For example 50h30m (note: max time unit is an hour so to
                set a day you should use 24h). It will be ceil rounded to the nearest amount of
                epoch. (default: 720h0m0s).
            container_policy: Mapping AWS storage class to FrostFS storage policy as plain json string
                or path to json file.
            aws_cli_credentials: Path to the aws cli credential file.

        Returns:
            Command's result.
        """
        return self._execute_with_password(
            "issue-secret",
            wallet_password,
            **{
                param: param_value
                for param, param_value in locals().items()
                if param not in ["self"]
            },
        )
