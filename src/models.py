class QueueItem:
    id: int
    data: str
    print_location: str
    print_location_mix: str
    n_mix: int = 0

    def __init__(self, queue_id: int, data: str, print_location: str, print_location_mix: str, n_mix: int):
        self.id = queue_id
        self.data = data
        self.print_location = print_location
        self.print_location_mix = print_location_mix
        self.n_mix = n_mix


class Printer:
    def __init__(self, printer_id: str):
        self.printer_id = printer_id

