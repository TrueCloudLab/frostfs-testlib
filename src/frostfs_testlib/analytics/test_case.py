import allure

from enum import Enum
from types import FunctionType

class TestCasePriority(Enum):
    HIGHEST = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

def __set_label__(name: str, value: str, allure_decorator: FunctionType = None):
    """
    Generic function for do not duplicate set label code in each decorator.
    We get decorated function as an object and set needed argument inside.

    Args:
        name: argument name to set into the function object
        value: argument value to set into the function object
        allure_decorator: allure decorator to decorate function and do not duplicate decorators with same value
    """
    def wrapper(decorated_func):
        if allure_decorator:
            decorated_func = allure_decorator(value)(decorated_func)
        setattr(decorated_func, name, value)
        return decorated_func

    return wrapper


def id(uuid: str):
    """
    Decorator for set test case ID which can be used as unique value due export into TMS.

    We prefer to use UUID4 format string for ID.
    ID have to be generated manually for each new test.

    Args:
        uuid: id to set as test_case_id into test function
    """
    return __set_label__("__test_case_id__", uuid)


def title(title: str):
    """
    Decorator for set test case title / name / summary / short description what we do.

    Args:
        title: string with title to set into test function
    """

    return __set_label__("__test_case_title__", title, allure.title)

def priority(priority: str):
    """
    Decorator for set test case title / name / summary / short description what we do.

    Args:
        priority: string with priority to set into test function
    """

    return __set_label__("__test_case_priority__", priority)


def suite_name(name: str):
    """
    Decorator for set test case suite name.
    Suite name is usually using in TMS for create structure of test cases.

    Args:
        name: string with test suite name for set into test function
    """

    return __set_label__("__test_case_suite_name__", name, allure.story)


def suite_section(name: str):
    """
    Decorator for set test case suite section.
    Suite section is usually using in TMS for create deep test cases structure.
    """
    return __set_label__("__test_case_suite_section__", name)
