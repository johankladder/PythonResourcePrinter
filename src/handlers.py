from enum import Enum

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
            response = self.network.get(
                url=self.address + "/json",
                handle=True
            )

            if response is not None:
                self.network.get(
                    url=self.address + "/win" + self.__get_api_values(
                        status=status,
                        is_on=response.json()['state']['on'] is True
                    ),
                    handle=True,
                )

        self.previous_status = status

    @staticmethod
    def __get_api_values(status: Status, is_on: bool = False) -> str:
        color_map = {
            Status.IDLE: "&PL=2",
            Status.ERROR: "&PL=3",
            Status.PRINTING: "&PL=4",
            Status.PINGING: "",
            Status.OFF: "&T=0",
            Status.ON: "&T=1&PL=5"
        }

        if status is not Status.ON:
            if is_on is False:
                return ""

        return color_map.get(status)


class StatusHandler:
    subscribers: [HandlerPublisher] = []

    def subscribe(self, publisher: HandlerPublisher):
        self.subscribers.append(publisher)

    def publish(self, status: Status):
        for publisher in self.subscribers:
            publisher.handle(status=status)



