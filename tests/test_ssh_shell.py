import os
from unittest import SkipTest, TestCase

from frostfs_testlib.shell.interfaces import CommandOptions, InteractiveInput
from frostfs_testlib.shell.ssh_shell import SSHShell

from tests.helpers import format_error_details, get_output_lines


def init_shell() -> SSHShell:
    host = os.getenv("SSH_SHELL_HOST")
    port = os.getenv("SSH_SHELL_PORT", "22")
    login = os.getenv("SSH_SHELL_LOGIN")
    private_key_path = os.getenv("SSH_SHELL_PRIVATE_KEY_PATH")
    private_key_passphrase = os.getenv("SSH_SHELL_PRIVATE_KEY_PASSPHRASE")

    if not all([host, login, private_key_path, private_key_passphrase]):
        # TODO: in the future we might use https://pypi.org/project/mock-ssh-server,
        # at the moment it is not suitable for us because of its issues with stdin
        raise SkipTest("SSH connection is not configured")

    return SSHShell(
        host=host,
        port=port,
        login=login,
        private_key_path=private_key_path,
        private_key_passphrase=private_key_passphrase,
    )


class TestSSHShellInteractive(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = init_shell()

    def test_command_with_one_prompt(self):
        script = "password = input('Password: '); print('\\n' + password)"

        inputs = [InteractiveInput(prompt_pattern="Password", input="test")]
        result = self.shell.exec(
            f'python3 -c "{script}"', CommandOptions(interactive_inputs=inputs)
        )

        self.assertEqual(0, result.return_code)
        self.assertEqual(["Password: test", "test"], get_output_lines(result))
        self.assertEqual("", result.stderr)

    def test_command_with_several_prompts(self):
        script = (
            "input1 = input('Input1: '); print('\\n' + input1); "
            "input2 = input('Input2: '); print('\\n' + input2)"
        )
        inputs = [
            InteractiveInput(prompt_pattern="Input1", input="test1"),
            InteractiveInput(prompt_pattern="Input2", input="test2"),
        ]

        result = self.shell.exec(
            f'python3 -c "{script}"', CommandOptions(interactive_inputs=inputs)
        )

        self.assertEqual(0, result.return_code)
        self.assertEqual(
            ["Input1: test1", "test1", "Input2: test2", "test2"], get_output_lines(result)
        )
        self.assertEqual("", result.stderr)

    def test_invalid_command_with_check(self):
        script = "invalid script"
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        with self.assertRaises(RuntimeError) as raised:
            self.shell.exec(f'python3 -c "{script}"', CommandOptions(interactive_inputs=inputs))

        error = format_error_details(raised.exception)
        self.assertIn("SyntaxError", error)
        self.assertIn("return code: 1", error)

    def test_invalid_command_without_check(self):
        script = "invalid script"
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        result = self.shell.exec(
            f'python3 -c "{script}"',
            CommandOptions(interactive_inputs=inputs, check=False),
        )
        self.assertIn("SyntaxError", result.stdout)
        self.assertEqual(1, result.return_code)

    def test_non_existing_binary(self):
        inputs = [InteractiveInput(prompt_pattern=".*", input="test")]

        with self.assertRaises(RuntimeError) as raised:
            self.shell.exec("not-a-command", CommandOptions(interactive_inputs=inputs))

        error = format_error_details(raised.exception)
        self.assertIn("return code: 127", error)


class TestSSHShellNonInteractive(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shell = init_shell()

    def test_correct_command(self):
        script = "print('test')"

        result = self.shell.exec(f'python3 -c "{script}"')

        self.assertEqual(0, result.return_code)
        self.assertEqual("test", result.stdout.strip())
        self.assertEqual("", result.stderr)

    def test_invalid_command_with_check(self):
        script = "invalid script"

        with self.assertRaises(RuntimeError) as raised:
            self.shell.exec(f'python3 -c "{script}"')

        error = format_error_details(raised.exception)
        self.assertIn("Error", error)
        self.assertIn("return code: 1", error)

    def test_invalid_command_without_check(self):
        script = "invalid script"

        result = self.shell.exec(f'python3 -c "{script}"', CommandOptions(check=False))

        self.assertEqual(1, result.return_code)
        # TODO: we have inconsistency with local shell here, the local shell captures error info
        # in stdout while ssh shell captures it in stderr
        self.assertIn("Error", result.stderr)

    def test_non_existing_binary(self):
        with self.assertRaises(RuntimeError) as exc:
            self.shell.exec("not-a-command")

        error = format_error_details(exc.exception)
        self.assertIn("Error", error)
        self.assertIn("return code: 127", error)
