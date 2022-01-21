class QueueItem:
    id: int
    data: str
    print_location: str

    def __init__(self, queue_id: int, data: str, print_location: str):
        self.id = queue_id
        self.data = data
        self.print_location = print_location


class Printer:
    def __init__(self, printer_id: str):
        self.printer_id = printer_id

