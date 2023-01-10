import traceback

from frostfs_testlib.shell.interfaces import CommandResult


def format_error_details(error: Exception) -> str:
    """Converts specified exception instance into a string.

    The resulting string includes error message and the full stack trace.

    Args:
        error: Exception to convert.

    Returns:
        String containing exception details.
    """
    detail_lines = traceback.format_exception(
        etype=type(error),
        value=error,
        tb=error.__traceback__,
    )
    return "".join(detail_lines)


def get_output_lines(result: CommandResult) -> list[str]:
    """Converts output of specified command result into separate lines.

    Whitespaces are trimmed, empty lines are excluded.

    Args:
        result: Command result which output should be converted.

    Returns:
        List of lines extracted from the output.
    """
    return [line.strip() for line in result.stdout.split("\n") if line.strip()]
