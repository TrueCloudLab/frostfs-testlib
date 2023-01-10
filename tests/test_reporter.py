from contextlib import AbstractContextManager
from types import TracebackType
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock

from frostfs_testlib.reporter import Reporter


class TestLocalShellInteractive(TestCase):
    def setUp(self):
        self.reporter = Reporter()

    def test_handler_step_is_invoked(self):
        handler = MagicMock()
        self.reporter.register_handler(handler)

        with self.reporter.step("test_step"):
            pass

        handler.step.assert_called_once_with("test_step")

    def test_two_handler_steps_are_invoked(self):
        handler1 = MagicMock()
        handler2 = MagicMock()

        self.reporter.register_handler(handler1)
        self.reporter.register_handler(handler2)

        with self.reporter.step("test_step"):
            pass

        handler1.step.assert_called_once_with("test_step")
        handler2.step.assert_called_once_with("test_step")

    def test_handlers_can_suppress_exception(self):
        handler1 = MagicMock()
        handler1.step = MagicMock(return_value=StubContext(suppress_exception=True))
        handler2 = MagicMock()
        handler2.step = MagicMock(return_value=StubContext(suppress_exception=True))

        self.reporter.register_handler(handler1)
        self.reporter.register_handler(handler2)

        with self.reporter.step("test_step"):
            raise ValueError("Test exception")

    def test_handler_can_override_exception_suppression(self):
        handler1 = MagicMock()
        handler1.step = MagicMock(return_value=StubContext(suppress_exception=True))
        handler2 = MagicMock()
        handler2.step = MagicMock(return_value=StubContext(suppress_exception=False))

        self.reporter.register_handler(handler1)
        self.reporter.register_handler(handler2)

        with self.assertRaises(ValueError):
            with self.reporter.step("test_step"):
                raise ValueError("Test exception")


class StubContext(AbstractContextManager):
    def __init__(self, suppress_exception: bool) -> None:
        super().__init__()
        self.suppress_exception = suppress_exception

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        return self.suppress_exception
