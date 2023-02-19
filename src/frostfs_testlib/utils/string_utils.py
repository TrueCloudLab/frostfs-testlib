import random
import re
import string

ONLY_ASCII_LETTERS = string.ascii_letters
DIGITS_AND_ASCII_LETTERS = string.ascii_letters + string.digits


def random_string(length: int = 5, source: str = ONLY_ASCII_LETTERS):
    """
    Generate random string from source letters list

    Args:
         length: length for generated string
         source: source string with letters for generate random string
    Returns:
        (str): random string with len == length
    """

    return "".join(random.choice(string.ascii_letters) for i in range(length))


def is_str_match_pattern(error: Exception, status_pattern: str) -> bool:
    """
    Determines whether exception matches specified status pattern.

    We use re.search() to be consistent with pytest.raises.
    """
    match = re.search(status_pattern, str(error))

    return match is not None
