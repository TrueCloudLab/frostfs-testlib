from testrail_api import TestRailAPI

from test_collector import TestCase
from test_exporter import TestExporter


class TestrailExporter(TestExporter):
    def __init__(
            self,
            tr_url: str,
            tr_username: str,
            tr_password: str,
            tr_project_id: int,
            tr_template_id_without_steps: int,
            tr_template_id_with_steps: int,
            tr_priority_map: dict,
            tr_id_field: str,
            tr_description_fields: str,
            tr_steps_field: str,
    ):
        """
        Redefine init for base exporter for get test rail credentials and project on create exporter

        Args:
            tr_url: api url for create TestRailAPI object. See lib docs for details
            tr_username: Testrail user login for api authentication
            tr_password: Testrail user password for api authentication
            tr_template_id_with_steps: id of test case template with steps
            tr_template_id_without_steps: id of test case template without steps
            tr_priority_map: mapping of TestCasePriority to priority ids in Testrail
        """

        self.api: TestRailAPI = TestRailAPI(tr_url, tr_username, tr_password)
        self.tr_project_id: int = tr_project_id
        self.tr_template_id_without_steps = tr_template_id_without_steps
        self.tr_template_id_with_steps = tr_template_id_with_steps
        self.tr_priority_map = tr_priority_map
        self.tr_id_field = tr_id_field
        self.tr_description_fields = tr_description_fields
        self.tr_steps_field = tr_steps_field

    def fill_suite_cache(self) -> None:
        """
        Fill test_suite_cache by all tests cases in TestRail
        It's help do not call TMS each time then we search test suite
        """
        project_suites = self.api.suites.get_suites(project_id=self.tr_project_id)

        for test_suite in project_suites:
            test_suite_sections = self.api.sections.get_sections(
                project_id=self.tr_project_id,
                suite_id=test_suite["id"],
            )
            test_suite["sections"] = test_suite_sections

            self.test_suites_cache.append(test_suite)

    def fill_cases_cache(self) -> None:
        """
        Fill test_cases_cache by all tests cases in TestRail
        It's help do not call TMS each time then we search test case
        """
        for test_suite in self.test_suites_cache:
            self.test_cases_cache.extend(
                self.api.cases.get_cases(self.tr_project_id, suite_id=test_suite["id"])
            )

    def search_test_case_id(self, test_case_id: str) -> object:
        """
        Find test cases in TestRail (cache) by ID
        """
        test_cases = [
            test_case
            for test_case in self.test_cases_cache
            if test_case["custom_autotest_name"] == test_case_id
        ]

        if len(test_cases) > 1:
            raise RuntimeError(f"Too many results found in test rail for id {test_case_id}")
        elif len(test_cases) == 1:
            return test_cases.pop()
        else:
            return None

    def get_or_create_test_suite(self, test_suite_name) -> object:
        """
        Get suite name with exact name from Testrail or create if not exist
        """
        test_rail_suites = [
            suite for suite in self.test_suites_cache if suite["name"] == test_suite_name
        ]

        if not test_rail_suites:
            test_rail_suite = self.api.suites.add_suite(
                project_id=self.tr_project_id,
                name=test_suite_name,
            )
            test_rail_suite["sections"] = list()
            self.test_suites_cache.append(test_rail_suite)
            return test_rail_suite
        elif len(test_rail_suites) == 1:
            return test_rail_suites.pop()
        else:
            raise RuntimeError(f"Too many results found in test rail for suite name {test_suite_name}")

    def get_or_create_suite_section(self, test_rail_suite, section_name) -> object:
        """
        Get suite section with exact name from Testrail or create new one if not exist
        """
        test_rail_sections = [
            section for section in test_rail_suite["sections"] if section["name"] == section_name
        ]

        if not test_rail_sections:
            test_rail_section = self.api.sections.add_section(
                project_id=self.tr_project_id,
                suite_id=test_rail_suite["id"],
                name=section_name,
            )
            # !!!!!! BAD !!!!!! Do we really change object from cache or copy of suite object????
            # !!!!!! WE have to update object in cache
            # !!!!!  In opposite we will try to create section twice and get error from API
            test_rail_suite["sections"].append(test_rail_section)
            return test_rail_section
        elif len(test_rail_sections) == 1:
            return test_rail_sections.pop()
        else:
            raise RuntimeError(
                f"Too many results found in test rail for section name {section_name}"
            )

    def prepare_request_body(self, test_case: TestCase, test_suite, test_suite_section) -> dict:
        """
        Helper to prepare request body for add or update tests case from TestCase object
        """
        request_body = {
            "title": test_case.title,
            "section_id": test_suite_section["id"],
            self.test_case_id_field_name: test_case.id,

        }

        if test_case.priority:
            request_body["priority_id"] = self.tr_priority_map.get(test_case.priority)

        if test_case.steps:
            steps = [
                {"content": value, "expected": " "}
                for key, value in test_case.steps.items()
            ]
            request_body[self.tr_steps_field] = steps
            request_body["template_id"]=self.tr_template_id_with_steps
        else:
            request_body["template_id"] = self.tr_template_id_without_steps
        if test_case.description:
            request_body[self.tr_description_fields] = self.tr_description_fields

        return request_body


    def create_test_case(self, test_case: TestCase, test_suite, test_suite_section) -> None:
        """
        Create test case in Testrail
        """
        request_body = self.prepare_request_body(test_case, test_suite, test_suite_section)

        self.api.cases.add_case(**request_body)


    def update_test_case(self, test_case: TestCase, test_case_in_tms, test_suite, test_suite_section) -> None:
        """
        Update test case in Testrail
        """
        request_body = self.prepare_request_body(test_case, test_suite, test_suite_section)

        self.api.cases.update_case(case_id=test_case_in_tms["id"], **request_body)


