from typing import Optional

from frostfs_testlib.shell import CommandOptions, CommandResult, InteractiveInput, Shell


class CliCommand:

    WALLET_SOURCE_ERROR_MSG = "Provide either wallet or wallet_config to specify wallet location"
    WALLET_PASSWD_ERROR_MSG = "Provide either wallet_password or wallet_config to specify password"

    cli_exec_path: Optional[str] = None
    __base_params: Optional[str] = None
    map_params = {
        "json_mode": "json",
        "await_mode": "await",
        "hash_type": "hash",
        "doc_type": "type",
        "to_address": "to",
        "from_address": "from",
        "to_file": "to",
        "from_file": "from",
    }

    def __init__(self, shell: Shell, cli_exec_path: str, **base_params):
        self.shell = shell
        self.cli_exec_path = cli_exec_path
        self.__base_params = " ".join(
            [f"--{param} {value}" for param, value in base_params.items() if value]
        )

    def _format_command(self, command: str, **params) -> str:
        param_str = []
        for param, value in params.items():
            if param == "post_data":
                param_str.append(value)
                continue
            if param in self.map_params.keys():
                param = self.map_params[param]
            param = param.replace("_", "-")
            if not value:
                continue
            if isinstance(value, bool):
                param_str.append(f"--{param}")
            elif isinstance(value, int):
                param_str.append(f"--{param} {value}")
            elif isinstance(value, list):
                for value_item in value:
                    val_str = str(value_item).replace("'", "\\'")
                    param_str.append(f"--{param} '{val_str}'")
            elif isinstance(value, dict):
                param_str.append(
                    f'--{param} \'{",".join(f"{key}={val}" for key, val in value.items())}\''
                )
            else:
                if "'" in str(value):
                    value_str = str(value).replace('"', '\\"')
                    param_str.append(f'--{param} "{value_str}"')
                else:
                    param_str.append(f"--{param} '{value}'")

        param_str = " ".join(param_str)

        return f"{self.cli_exec_path} {self.__base_params} {command or ''} {param_str}"

    def _execute(self, command: Optional[str], **params) -> CommandResult:
        return self.shell.exec(self._format_command(command, **params))

    def _execute_with_password(self, command: Optional[str], password, **params) -> CommandResult:
        return self.shell.exec(
            self._format_command(command, **params),
            options=CommandOptions(
                interactive_inputs=[InteractiveInput(prompt_pattern="assword", input=password)]
            ),
        )
