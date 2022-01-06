class QueueItem:
    id: int
    data: str

    def __init__(self, queue_id: int, data: str):
        self.id = queue_id
        self.data = data
