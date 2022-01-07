import requests
from src.models import QueueItem


class Network:

    def get(self, url: str):
        return requests.get(url)

    def patch(self, url: str):
        return requests.patch(url)


class PrinterQueueNetwork:

    base_64_key = "label_base64"
    id_key = "id"

    def __init__(self, base_url: str, auth_token: str, network=Network()):
        self.base_url = base_url
        self.network = network
        self.auth_token = auth_token

    def get_queue(self):
        items = []
        for item in self.network.get(self.base_url + self.get_authentication_end_fix()).json()["data"]:
            items.append(QueueItem(queue_id=item[self.id_key], data=item[self.base_64_key]))
        return items

    def set_printed(self, item: QueueItem):
        return self.network.patch(self.base_url + "/" + str(item.id) + self.get_authentication_end_fix())

    def get_authentication_end_fix(self):
        return "?key=" + self.auth_token
