import re


def error_matches_status(error: Exception, status_pattern: str) -> bool:
    """
    Determines whether exception matches specified status pattern.

    We use re.search() to be consistent with pytest.raises.
    """
    match = re.search(status_pattern, str(error))
    return match is not None
