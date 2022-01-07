import datetime
import subprocess
import fire
import time
from dotenv import load_dotenv
import os
from src.filesystem import FileSystem
from src.network import PrinterQueueNetwork, Network
from src.parser import PdfParser


class CommandReceiver(object):

    tmp_file = "tmp.pdf"
    network = Network()
    last_ping = datetime.datetime.now()

    def __init__(self):
        load_dotenv()
        self.queue_network = PrinterQueueNetwork(
            base_url=os.getenv("PRINT_QUEUE_BASE_URL"),
            auth_token=os.getenv("AUTH_TOKEN"),
            network=self.network
        )
        self.ping_url = os.getenv("PING_URL")

    def listen(self, delay=2, ping_minutes=5):
        print("Initialised printing server for url: ", self.queue_network.base_url)
        print("Print server started - polling every " + str(delay) + " seconds")

        while True:
            queue_items = self.queue_network.get_queue()
            self.__ping(ping_minutes)

            if len(queue_items) > 0:
                print(str(len(queue_items)) + " queue-items found")

            for item in queue_items:

                # Parse bytes of base64:
                pdf_bytes = PdfParser.parse(base64=item.data)

                # If bytes couldn't be formed - jump out:
                if pdf_bytes is None:
                    continue

                # Write to temporary .pdf file:
                FileSystem.write_file(path=self.tmp_file, file_bytes=pdf_bytes)

                # Print the pdf file:
                subprocess.run(["lp", self.tmp_file, os.getenv("LP_OPTIONS")])

                # Remove the temporary file:
                FileSystem.remove_file(path=self.tmp_file)

                # Send status to server:
                self.queue_network.set_printed(item)

            time.sleep(delay)

    def __ping(self, minutes: int):
        if self.ping_url:
            current_time = datetime.datetime.now()
            minutes_passed = current_time - self.last_ping
            if minutes_passed.total_seconds() / 60 >= minutes:
                self.last_ping = current_time
                self.network.get(self.ping_url)
                print("- Pinged to the pinging url")


if __name__ == '__main__':
    fire.Fire(CommandReceiver)
