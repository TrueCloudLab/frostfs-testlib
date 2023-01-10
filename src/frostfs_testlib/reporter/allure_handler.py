import os
from contextlib import AbstractContextManager
from textwrap import shorten
from typing import Any

import allure
from allure import attachment_type

from frostfs_testlib.reporter.interfaces import ReporterHandler


class AllureHandler(ReporterHandler):
    """Handler that stores test artifacts in Allure report."""

    def step(self, name: str) -> AbstractContextManager:
        name = shorten(name, width=70, placeholder="...")
        return allure.step(name)

    def attach(self, body: Any, file_name: str) -> None:
        attachment_name, extension = os.path.splitext(file_name)
        attachment_type = self._resolve_attachment_type(extension)

        allure.attach(body, attachment_name, attachment_type, extension)

    def _resolve_attachment_type(self, extension: str) -> attachment_type:
        """Try to find matching Allure attachment type by extension.

        If no match was found, default to TXT format.
        """
        extension = extension.lower()
        return next(
            (allure_type for allure_type in attachment_type if allure_type.extension == extension),
            attachment_type.TEXT,
        )
