from typing import Optional
import requests
from requests import RequestException, Response
from src.models import QueueItem


class Network:

    def get(self, url: str, handle: bool = True) -> Optional[Response]:
        if handle is False:
            return requests.get(url)

        try:
            return requests.get(url)
        except RequestException as e:
            return self.__handle_exception(url, e)

    def patch(self, url: str) -> Optional[Response]:
        try:
            return requests.patch(url)
        except RequestException as e:
            return self.__handle_exception(url, e)

    @staticmethod
    def __handle_exception(url: str, e: RequestException):
        print("Request failed for", url, e)
        return None


class PrinterQueueNetwork:

    base_64_key = "label_base64"
    id_key = "id"
    print_location_key = "print_location"
    print_location_mix_key = "print_location_mix"
    n_mix = "n_mix"

    def __init__(self, base_url: str, auth_token: str, network=Network()):
        self.base_url = base_url
        self.network = network
        self.auth_token = auth_token

    def get_queue(self) -> [QueueItem]:
        items = []

        for item in self.network.get(self.base_url + self.get_authentication_end_fix(), handle=False).json()["data"]:
            items.append(QueueItem(
                    queue_id=item[self.id_key],
                    data=item[self.base_64_key],
                    print_location=item.get(self.print_location_key, None),
                    print_location_mix=item.get(self.print_location_mix_key, item.get(self.print_location_key, None)),
                    n_mix=item.get(self.n_mix, 0)
                )
            )
        return items

    def set_printed(self, item: QueueItem) -> bool:
        try:
            self.network.patch(self.base_url + "/" + str(item.id) + self.get_authentication_end_fix())
            return True
        finally:
            return False

    def get_authentication_end_fix(self):
        return "?key=" + self.auth_token
