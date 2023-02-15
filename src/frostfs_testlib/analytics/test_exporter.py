from abc import ABC, abstractmethod

from test_collector import TestCase

class TestExporter(ABC):
    test_cases_cache = []
    test_suites_cache = []
    test_case_id_field_name = ""

    @abstractmethod
    def fill_suite_cache(self) -> None:
        """
        Fill test_suite_cache by all tests cases in TMS
        It's help do not call TMS each time then we search test suite
        """

    @abstractmethod
    def fill_cases_cache(self) -> None:
        """
        Fill test_cases_cache by all tests cases in TMS
        It's help do not call TMS each time then we search test case
        """

    @abstractmethod
    def search_test_case_id(self, test_case_id: str) -> object:
        """
        Find test cases in TMS by ID
        """

    @abstractmethod
    def get_or_create_test_suite(self, test_suite_name) -> object:
        """
        Get suite name with exact name or create if not exist
        """

    @abstractmethod
    def get_or_create_suite_section(self, test_rail_suite, section_name) -> object:
        """
        Get suite section with exact name or create new one if not exist
        """

    @abstractmethod
    def create_test_case(self, test_case: TestCase, test_suite, test_suite_section) -> None:
        """
        Create test case in TMS
        """

    @abstractmethod
    def update_test_case(self, test_case: TestCase, test_case_in_tms, test_suite, test_suite_section) -> None:
        """
        Update test case in TMS
        """

    def export_test_cases(self, test_cases: list[TestCase]):
        # Fill caches before starting imports
        self.fill_suite_cache()
        self.fill_cases_cache()

        for test_case in test_cases:
            test_suite = self.get_or_create_test_suite(test_case.suite_name)
            test_section = self.get_or_create_suite_section(test_suite, test_case.suite_section_name)
            test_case_in_tms = self.search_test_case_id(test_case.id)
            steps = [
                {"content": value, "expected": " "}
                for key, value in test_case.steps.items()
            ]

            if test_case:
                self.update_test_case(test_case, test_case_in_tms)
            else:
                self.create_test_case(test_case)