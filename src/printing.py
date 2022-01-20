import os
import subprocess


class Printer:
    def __init__(self, printer_id: str):
        self.printer_id = printer_id


class Printing:

    @staticmethod
    def print(file_path: str, printer: Printer):
        printer_option = Printing.get_specific_printer_option(printer)
        command = ["lp", file_path, os.getenv("LP_OPTIONS") + printer_option]
        print(command)
        subprocess.check_call(command)

    @staticmethod
    def get_printer_based_on_location(printer_location: str) -> Printer:
        default_printer_id = os.getenv("PRINTER_LOCATION_DEFAULT", None)

        # Check if the printer location is defined is set up:
        if printer_location is not None:
            printer_id = os.getenv("PRINTER_LOCATION_" + str(printer_location), None)
            if printer_id is not None:
                return Printer(printer_id=printer_id)
            else:
                print("Cannot find printer location " + str(printer_location))

        # If not defined, use default printer:
        if default_printer_id is not None:
            print("Using default printer")
            return Printer(printer_id=default_printer_id)

    @staticmethod
    def get_specific_printer_option(printer: Printer) -> str:
        return " -d " + printer.printer_id

