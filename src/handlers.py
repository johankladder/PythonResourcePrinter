from enum import Enum
import asyncio
from wled import WLED

from src.network import Network


class Status(Enum):
    IDLE = 1
    PRINTING = 2
    ERROR = 3
    PINGING = 4
    ON = 5
    OFF = 6


class HandlerPublisher:

    def handle(self, status: Status):
        pass


class DebugPublisher(HandlerPublisher):

    def handle(self, status: Status):
        messages = {
            Status.IDLE: "IDLE",
            Status.PRINTING: "PRINTING",
            Status.ERROR: "ERROR",
            Status.PINGING: "PINGING"
        }

        readable_status = messages.get(status)
        if readable_status is not None:
            print("Debugging - status: " + readable_status)


class WLEDPublisher(HandlerPublisher):

    network = Network()
    address: str
    previous_status: Status = None

    def handle(self, status: Status):
        if self.previous_status is not status:
            self.network.get(
                url=self.address + "/win" + self.__get_api_values(status),
                handle=True
            )
            self.previous_status = status

    @staticmethod
    def __get_api_values(status: Status) -> str:
        color_map = {
            Status.IDLE: "&R=0&G=255&B=0&FX=0",
            Status.ERROR: "&R=255&G=0&B=0&FX=0",
            Status.PRINTING: "&R=255&G=165&B=0&FX=74&SX=128&IX=100",
            Status.PINGING: "&R=0&G=0&B=255&FX=0",
            Status.OFF: "&T=0",
            Status.ON: "&T=1&FX=50&SX=84&CL=h00FF00&C2=000000&C3=000000"
        }
        return "&A=255" + color_map.get(status)


class StatusHandler:
    subscribers: [HandlerPublisher] = []

    def subscribe(self, publisher: HandlerPublisher):
        self.subscribers.append(publisher)

    def publish(self, status: Status):
        for publisher in self.subscribers:
            publisher.handle(status=status)



