import datetime
import subprocess
import fire
import time
from dotenv import load_dotenv
import os
from requests import RequestException
from src.filesystem import FileSystem
from src.handlers import StatusHandler, DebugPublisher, Status
from src.network import PrinterQueueNetwork, Network
from src.parser import PdfParser
from distutils.util import strtobool
from src.printing import Printing, Printer


class CommandReceiver(object):
    debug_publisher = DebugPublisher()

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
        self.__initialise_status_handler()

    def __initialise_status_handler(self):
        self.status_handler = StatusHandler()
        self.status_handler.subscribe(publisher=self.debug_publisher)

    def print(self, path: str, destination=None):
        self.status_handler.publish(status=Status.IDLE)
        queue_printer = Printing.get_printer_based_on_location(printer_location=destination)

        if queue_printer is not None and path is not None:
            print("Using printer: " + queue_printer.printer_id)
            self.status_handler.publish(status=Status.PRINTING)
            Printing.print(file_path=path, printer=queue_printer)

        self.status_handler.publish(status=Status.IDLE)

    def split(self, path: str, n_mix: int = 0):
        paths = PdfParser.split_pdf(base_path=path, split_at_page=n_mix)
        print(paths)

    def listen(self, delay=2, ping_minutes=1):
        print("Initialised printing server for url: ", self.queue_network.base_url)
        print("Print server started - polling every " + str(delay) + " seconds")

        while True:
            try:
                queue_items = self.queue_network.get_queue()
            except RequestException:
                self.status_handler.publish(status=Status.ERROR)
                time.sleep(2)
                continue

            self.__ping(ping_minutes)
            self.status_handler.publish(status=Status.IDLE)

            if len(queue_items) > 0:
                print(str(len(queue_items)) + " queue-items found")

            for item in queue_items:
                # Parse bytes of base64:
                pdf_bytes = PdfParser.parse(base64=item.data)

                # If bytes couldn't be formed - jump out:
                if pdf_bytes is None:
                    continue

                # Retrieve printers:
                queue_printers: [str, Printer] = Printing.get_printers(item)
                if queue_printers['default'] is None:
                    print("No suitable default printer was found. Please define a printer location or default printer")
                    continue

                # Define printers:
                default_printer = queue_printers['default']
                mix_printer = queue_printers['mix']

                # Generate file_paths:
                file_path_tmp = FileSystem.generate_file_path(queue_item_id=item.id)

                # Write to temporary .pdf file:
                FileSystem.write_file(path=file_path_tmp, file_bytes=pdf_bytes)

                # Split temporary file in mix and default:
                paths = PdfParser.split_pdf(base_path=file_path_tmp, split_at_page=item.n_mix)

                # Print the pdf file and send status:
                try:
                    if self.debug is False:
                        if paths[0] is not None and item.print_items is True:
                            self.__handle_print(pdf_path=paths[0], printer=default_printer)
                        if len(paths) > 1 and paths[1] is not None and item.print_mix is True:
                            self.__handle_print(pdf_path=paths[1], printer=mix_printer)
                        self.queue_network.set_printed(item)

                except subprocess.CalledProcessError as e:
                    print("Some error did occur when trying to print", e)
                    self.status_handler.publish(status=Status.ERROR)
                    time.sleep(0.5)
                finally:
                    print("Printed item with id: " + str(item.id))

            time.sleep(delay)

    def __handle_print(self, pdf_path: str, printer: Printer):
        self.status_handler.publish(status=Status.PRINTING)
        Printing.print(file_path=pdf_path, printer=printer)

    def __ping(self, minutes: int):
        if self.ping_url and self.debug is False:
            current_time = datetime.datetime.now()
            minutes_passed = current_time - self.last_ping
            if minutes_passed.total_seconds() / 60 >= minutes:
                self.last_ping = current_time
                self.network.get(self.ping_url)
                self.status_handler.publish(status=Status.PINGING)


if __name__ == '__main__':
    fire.Fire(CommandReceiver())
