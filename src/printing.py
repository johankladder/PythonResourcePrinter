import os
import subprocess


class Printer:
    def __init__(self, printer_id: str):
        self.printer_id = printer_id


class Printing:

    @staticmethod
    def print(file_path: str, printer: Printer = None):
        printer_option = Printing.get_specific_printer_option(printer)
        subprocess.check_call(["lp", file_path, os.getenv("LP_OPTIONS"), printer_option])

    @staticmethod
    def get_printer_based_on_location(printer_location: str) -> Printer:
        if printer_location is not None:
            printer_id = os.getenv("PRINTER_LOCATION_" + printer_location, None)
            if printer_id is not None:
                return Printer(printer_id=printer_id)

    @staticmethod
    def get_specific_printer_option(printer: Printer = None) -> str:
        if printer is not None:
            return "-d " + printer.printer_id
        return ""

