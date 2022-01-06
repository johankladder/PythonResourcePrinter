import subprocess
import fire
import time
from dotenv import load_dotenv
import os
from src.filesystem import FileSystem
from src.network import PrinterQueueNetwork
from src.parser import PdfParser


class CommandReceiver(object):

    def __init__(self):
        load_dotenv()
        self.queue_network = PrinterQueueNetwork(
            base_url=os.getenv("PRINT_QUEUE_BASE_URL"),
            auth_token=os.getenv("AUTH_TOKEN")
        )
        self.parser = PdfParser()
        self.file_system = FileSystem()
        self.tmp_file = "tmp.pdf"

    def listen(self, delay=2):
        print("Initialised printing server for url: ", self.queue_network.base_url)
        print("Print server started - polling every " + str(delay) + " seconds")

        while True:
            queue_items = self.queue_network.get_queue()

            if len(queue_items) > 0:
                print("Polling succeeded " + str(len(queue_items)) + " found...")

            for item in queue_items:

                # Parse bytes of base64:
                pdf_bytes = self.parser.parse(base64=item.data)

                # If bytes couldn't be formed - jump out:
                if pdf_bytes is None:
                    continue

                # Write to temporary .pdf file:
                self.file_system.write_file(path=self.tmp_file, file_bytes=pdf_bytes)

                # Print the pdf file:
                subprocess.run(["lp", self.tmp_file, os.getenv("LP_OPTIONS")])

                # Remove the temporary file:
                self.file_system.remove_file(path=self.tmp_file)

                # Send status to server:
                self.queue_network.set_printed(item)

            time.sleep(delay)


if __name__ == '__main__':
    fire.Fire(CommandReceiver)
