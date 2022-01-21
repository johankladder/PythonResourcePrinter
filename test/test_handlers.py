from src.handlers import StatusHandler, Status, HandlerPublisher
from unittest.mock import MagicMock


def test_publish_empty_status_handler():
    status_handler = StatusHandler()
    a_publisher = HandlerPublisher()
    a_publisher.handle = MagicMock()
    status_handler.publish(status=Status.IDLE)
    a_publisher.handle.assert_not_called()


def test_publish_status_handler():
    status_handler = StatusHandler()
    a_publisher = HandlerPublisher()
    a_publisher.handle = MagicMock()
    status_handler.subscribe(publisher=a_publisher)
    status_handler.publish(status=Status.IDLE)
    a_publisher.handle.assert_called_once()


def test_publish_status_handler_multiple():
    status_handler = StatusHandler()
    a_publisher = HandlerPublisher()
    b_publisher = HandlerPublisher()
    a_publisher.handle = MagicMock()
    b_publisher.handle = MagicMock()
    status_handler.subscribe(publisher=a_publisher)
    status_handler.subscribe(publisher=b_publisher)
    status_handler.publish(status=Status.IDLE)
    a_publisher.handle.assert_called_once()
    b_publisher.handle.assert_called_once()


