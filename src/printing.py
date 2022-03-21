import os

from src.models import Printer, QueueItem


class Printing:

    @staticmethod
    def print(file_path: str, printer: Printer):
        printer_option = Printing.get_specific_printer_option(printer)
        commands = ["lp", file_path, Printing.get_general_printing_option(printer) + printer_option]
        command = " ".join(commands)
        os.system(command)

    @staticmethod
    def get_printer_based_on_location(printer_location: str) -> Printer:
        default_printer_id = os.getenv("PRINTER_LOCATION_DEFAULT", None)

        # Check if the printer location is defined is set up:
        if printer_location is not None:
            printer_id = os.getenv("PRINTER_LOCATION_" + str(printer_location), None)
            if printer_id is not None:
                return Printer(printer_id=printer_id, printer_location=printer_location)
            else:
                print("Cannot find printer location " + str(printer_location))

        # If not defined, use default printer:
        if default_printer_id is not None:
            print("Using default printer")
            return Printer(printer_id=default_printer_id)

    @staticmethod
    def get_printers(item: QueueItem) -> [str, Printer]:
        return {
            'default': Printing.get_printer_based_on_location(printer_location=item.print_location),
            'mix': Printing.get_printer_based_on_location(printer_location=item.print_location_mix),
        }

    @staticmethod
    def get_specific_printer_option(printer: Printer) -> str:
        return " -d " + printer.printer_id

    @staticmethod
    def get_general_printing_option(printer: Printer) -> str:
        default_lp_options = os.getenv("LP_OPTIONS")
        location = printer.printer_location

        if location is not None:
            location_lp_options = os.getenv("LP_OPTIONS_" + location)
            if location_lp_options is not None:
                return location_lp_options

        # Fallback:
        return default_lp_options

