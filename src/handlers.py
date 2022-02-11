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
    preset_map = {
        Status.IDLE: 2,
        Status.ERROR: 3,
        Status.PRINTING: 4,
        Status.ON: 5,
        Status.OFF: 6,
        Status.PINGING: 7,
    }

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
                        is_on=response.json()['state']['on'] is True,
                        current_preset=response.json()['state']['ps']
                    ),
                    handle=True,
                )

        self.previous_status = status

    def __get_api_values(self, status: Status, is_on: bool, current_preset: int) -> str:
        if status is not Status.ON:
            if is_on is False:
                return ""

        api_values = ""
        preset = self.preset_map.get(status)
        if preset is not None:
            api_values += ("&PL=" + str(preset))

        if status is Status.ON:
            api_values += "&T=1"

        if preset == current_preset:
            return ""

        return api_values


class StatusHandler:
    subscribers: [HandlerPublisher] = []

    def subscribe(self, publisher: HandlerPublisher):
        self.subscribers.append(publisher)

    def publish(self, status: Status):
        for publisher in self.subscribers:
            publisher.handle(status=status)
