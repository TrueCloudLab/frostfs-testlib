from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any


class ReporterHandler(ABC):
    """Interface of handler that stores test artifacts in some reporting tool."""

    @abstractmethod
    def step(self, name: str) -> AbstractContextManager:
        """Register a new step in test execution.

        Args:
            name: Name of the step.

        Returns:
            Step context.
        """

    @abstractmethod
    def attach(self, content: Any, file_name: str) -> None:
        """Attach specified content with given file name to the test report.

        Args:
            content: Content to attach. If content value is not a string, it will be
                converted to a string.
            file_name: File name of attachment.
        """
