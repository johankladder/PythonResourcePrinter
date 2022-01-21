from enum import Enum


class Status(Enum):
    IDLE = 1
    PRINTING = 2
    ERROR = 3


class StatusHandler:
    subscribers = []


class HandlerPublisher:

    def handle(self, status: Status):
        pass


class DebugPublisher(HandlerPublisher):

    def handle(self, status: Status):
        print("DEBUG")
