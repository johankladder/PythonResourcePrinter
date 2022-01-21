from enum import Enum


class Status(Enum):
    IDLE = 1
    PRINTING = 2
    ERROR = 3


class HandlerPublisher:

    def handle(self, status: Status):
        pass


class DebugPublisher(HandlerPublisher):

    def handle(self, status: Status):
        messages = {
            Status.IDLE: "IDLE",
            Status.PRINTING: "PRINTING",
            Status.ERROR: "ERROR"
        }
        print("Debugging - Printer status: " + messages[status])


class StatusHandler:
    subscribers: [HandlerPublisher] = []

    def subscribe(self, publisher: HandlerPublisher):
        self.subscribers.append(publisher)

    def publish(self, status: Status):
        for publisher in self.subscribers:
            publisher.handle(status=status)



