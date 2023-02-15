import re

from docstring_parser import parse
from docstring_parser.common import DocstringStyle
from docstring_parser.google import DEFAULT_SECTIONS, Section, SectionType

DEFAULT_SECTIONS.append(Section("Steps", "steps", SectionType.MULTIPLE))

class TestCase:
    """
    Test case object implementation for use in collector and exporters
    """

    def __init__(
        self,
        uuid_id: str,
        title: str,
        description: str,
        priority: int,
        steps: dict,
        params: str,
        suite_name: str,
        suite_section_name: str,
    ):
        """
        Base constructor for TestCase object

        Args:
            uuid_id: uuid from id decorator
            title: test case title from title decorator
            priority: test case priority value (0-3)
            steps: list of test case steps read from function __doc__
            params: string with test case param read from pytest Function(test) object
            suite_name: test case suite name from test_suite decorator
            suite_section_name: test case suite section from test_suite_section decorator
        """

        # It can confuse, but we rewrite id to "id [params]" string
        # We do it in case that one functions can return a lot of tests if we use test params
        if params:
            self.id = f"{uuid_id} [{params}]"
        else:
            self.id: str = uuid_id
        self.title: str = title
        self.description: str = description
        self.priority: int = priority
        self.steps: dict = steps
        self.params: str = params
        self.suite_name: str = suite_name
        self.suite_section_name: str = suite_section_name


class TestCaseCollector:
    """
    Collector working like a plugin for pytest and can be used in collect-only call to get tests list from pytest
    Additionally, we have several function to filter tests that can be exported.
    """

    pytest_tests = []

    def __format_string_with_params__(self, source_string: str, test_params: dict) -> str:
        """
        Helper function for format test case string arguments using test params.
        Params name can be deep like a.b.c, so we will get the value from tests params.
        Additionally, we check is the next object dict or real object to use right call for get next argument.

        Args:
            source_string: string for format by using test params (if needed)
            test_params: dictionary with test params got from pytest test object
        Returns:
            (str): formatted string with replaced params name by params value
        """

        target_string: str = source_string
        for match in re.findall(r"\{(.*?)}", source_string):
            nestings_attrs = match.split(".")
            param = None
            for nesting_attr in nestings_attrs:
                if not param:
                    param = test_params.get(nesting_attr)
                else:
                    if isinstance(param, dict):
                        param = param.get(nesting_attr)
                    else:
                        param = getattr(param, nesting_attr)
            target_string = target_string.replace(f"{{{match}}}", str(param))
        return target_string

    def __get_test_case_from_pytest_test__(self, test) -> TestCase:
        """
        Parce test meta and return test case if there is enough information for that.

        Args:
            test: pytest Function object
        Returns:
            (TestCase): return tests cases if there is enough information for that and None if not
        """

        # Default values for use behind
        suite_name: str = None
        suite_section_name: str = None
        test_case_steps = dict()
        test_case_params: str = ""
        test_case_description: str = ""

        # Read test_case suite and section name from test class if possible and get test function from class
        if test.cls:
            suite_name = test.cls.__dict__.get("__test_case_suite_name__", suite_name)
            suite_section_name = test.cls.__dict__.get("__test_case_suite_section__", suite_section_name)
            test_function = test.cls.__dict__[test.originalname]
        else:
            # If no test class, read test function from module
            test_function = test.module.__dict__[test.originalname]

        # Read base values from test function arguments
        test_case_id = test_function.__dict__.get("__test_case_id__", None)
        test_case_title = test_function.__dict__.get("__test_case_title__", None)
        test_case_priority = test_function.__dict__.get("__test_case_priority__", None)
        suite_name = test_function.__dict__.get("__test_case_suite_name__", suite_name)
        suite_section_name = test_function.__dict__.get("__test_case_suite_section__", suite_section_name)

        # Parce test_steps if they define in __doc__
        doc_string = parse(test_function.__doc__, style=DocstringStyle.GOOGLE)

        if doc_string.short_description:
            test_case_description = doc_string.short_description
            if doc_string.long_description:
                test_case_description = f"{doc_string.short_description}\r\n{doc_string.long_description}"

        if doc_string.meta:
            for meta in doc_string.meta:
                if meta.args[0] == "steps":
                    test_case_steps[meta.args[1]] = meta.description

        # Read params from tests function if its exist
        test_case_call_spec = getattr(test, "callspec", "")

        if test_case_call_spec:
            # Set test cases params string value
            test_case_params = test_case_call_spec.id
            # Format title with params
            if test_case_title:
                test_case_title = self.__format_string_with_params__(test_case_title,test_case_call_spec.params)
            # Format steps with params
            if test_case_steps:
                for key, value in test_case_steps.items():
                    value = self.__format_string_with_params__(value,test_case_call_spec.params)
                    test_case_steps[key] = value

        # If there is set basic test case attributes create TestCase and return
        if test_case_id and test_case_title and suite_name and suite_name:
            test_case = TestCase(
                            id=test_case_id,
                            title=test_case_title,
                            description=test_case_description,
                            priority=test_case_priority,
                            steps=test_case_steps,
                            params=test_case_params,
                            suite_name=suite_name,
                            suite_section_name=suite_section_name,
                        )
            return test_case
        # Return None if there is no enough information for return test case
        return None

    def pytest_report_collectionfinish(self, pytest_tests: list) -> None:
        """
        !!! DO NOT CHANGE THE NANE IT IS NOT A MISTAKE
        Implement specific function with specific name
        Pytest  will be call this function when he uses plugin in collect-only call

        Args:
            pytest_tests: list of pytest tests
        """
        self.pytest_tests.extend(pytest_tests)

    def collect_test_cases(self) -> list[TestCase]:
        """
        We're collecting test cases from the pytest tests list and return them in test case representation.

        Returns:
            (list[TestCase]): list of test cases that we found in the pytest tests code
        """
        test_cases = []

        for test in self.pytest_tests:
            test_case = self.__get_test_case_from_pytest_test__(test)
            if test_case:
                test_cases.append(test_case)
        return test_cases