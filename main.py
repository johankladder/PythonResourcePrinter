import datetime
import subprocess
import fire
import time
from dotenv import load_dotenv
import os
from src.filesystem import FileSystem
from src.models import QueueItem
from src.network import PrinterQueueNetwork, Network
from src.parser import PdfParser
from distutils.util import strtobool
from src.printing import Printing


class CommandReceiver(object):

    def __init__(self):
        load_dotenv()
        self.last_ping = datetime.datetime.now()
        self.network = Network()
        self.queue_network = PrinterQueueNetwork(
            base_url=os.getenv("PRINT_QUEUE_BASE_URL"),
            auth_token=os.getenv("AUTH_TOKEN"),
            network=self.network
        )
        self.debug = bool(strtobool(os.getenv('DEBUG', 'False')))
        self.ping_url = os.getenv("PING_URL")

    def listen(self, delay=2, ping_minutes=1):
        print("Initialised printing server for url: ", self.queue_network.base_url)
        print("Print server started - polling every " + str(delay) + " seconds")

        if self.debug is True:
            print("Debug mode is on")

        while True:
            queue_items = self.queue_network.get_queue()
            self.__ping(ping_minutes)

            if len(queue_items) > 0:
                print(str(len(queue_items)) + " queue-items found")
            else:
                print("No print jobs found!")

            for item in queue_items:
                # Parse bytes of base64:
                pdf_bytes = PdfParser.parse(base64=item.data)

                # If bytes couldn't be formed - jump out:
                if pdf_bytes is None:
                    continue

                # Generate file_path:
                file_path = FileSystem.generate_file_path(queue_item_id=item.id)

                # Write to temporary .pdf file:
                FileSystem.write_file(path=file_path, file_bytes=pdf_bytes)

                # Print the pdf file and send status:
                try:
                    if self.debug is False:
                        self.__handle_print(item, pdf_path=file_path)

                except subprocess.CalledProcessError:
                    print("Some error did occur when trying to print")
                finally:
                    print("Printed item with id: " + str(item.id))

            time.sleep(delay)

    def __handle_print(self, item: QueueItem, pdf_path: str):
        queue_printer = Printing.get_printer_based_on_location(printer_location=item.print_location)
        Printing.print(file_path=pdf_path, printer=queue_printer)
        self.queue_network.set_printed(item)

    def __ping(self, minutes: int):
        if self.ping_url and self.debug is False:
            current_time = datetime.datetime.now()
            minutes_passed = current_time - self.last_ping
            if minutes_passed.total_seconds() / 60 >= minutes:
                self.last_ping = current_time
                self.network.get(self.ping_url)
                print("- Pinged to the pinging url")


if __name__ == '__main__':
    fire.Fire(CommandReceiver())
