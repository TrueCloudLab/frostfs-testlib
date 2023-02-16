class Options:
    DEFAULT_SHELL_TIMEOUT = 90

    @staticmethod
    def get_default_shell_timeout():
        return Options.DEFAULT_SHELL_TIMEOUT

    @staticmethod
    def set_default_shell_timeout(value: int):
        Options.DEFAULT_SHELL_TIMEOUT = value
