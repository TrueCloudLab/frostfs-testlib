from contextlib import AbstractContextManager, contextmanager
from types import TracebackType
from typing import Any, Optional

from frostfs_testlib.plugins import load_plugin
from frostfs_testlib.reporter.interfaces import ReporterHandler


@contextmanager
def _empty_step():
    yield


class Reporter:
    """Root reporter that sends artifacts to handlers."""

    handlers: list[ReporterHandler]

    def __init__(self) -> None:
        super().__init__()
        self.handlers = []

    def register_handler(self, handler: ReporterHandler) -> None:
        """Register a new handler for the reporter.

        Args:
            handler: Handler instance to add to the reporter.
        """
        self.handlers.append(handler)

    def configure(self, config: dict[str, Any]) -> None:
        """Configure handlers in the reporter from specified config.

        All existing handlers will be removed from the reporter.

        Args:
            config: Dictionary with reporter configuration.
        """
        # Reset current configuration
        self.handlers = []

        # Setup handlers from the specified config
        handler_configs = config.get("handlers", [])
        for handler_config in handler_configs:
            handler_class = load_plugin("frostfs.testlib.reporter", handler_config["plugin_name"])
            self.register_handler(handler_class())

    def step(self, name: str) -> AbstractContextManager:
        """Register a new step in test execution.

        Args:
            name: Name of the step.

        Returns:
            Step context.
        """
        if not self.handlers:
            return _empty_step()

        step_contexts = [handler.step(name) for handler in self.handlers]
        return AggregateContextManager(step_contexts)

    def attach(self, content: Any, file_name: str) -> None:
        """Attach specified content with given file name to the test report.

        Args:
            content: Content to attach. If content value is not a string, it will be
                converted to a string.
            file_name: File name of attachment.
        """
        for handler in self.handlers:
            handler.attach(content, file_name)


class AggregateContextManager(AbstractContextManager):
    """Aggregates multiple context managers in a single context."""

    contexts: list[AbstractContextManager]

    def __init__(self, contexts: list[AbstractContextManager]) -> None:
        super().__init__()
        self.contexts = contexts

    def __enter__(self):
        for context in self.contexts:
            context.__enter__()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        suppress_decisions = []
        for context in self.contexts:
            suppress_decision = context.__exit__(exc_type, exc_value, traceback)
            suppress_decisions.append(suppress_decision)

        # If all context agreed to suppress exception, then suppress it;
        # otherwise return None to reraise
        return True if all(suppress_decisions) else None
