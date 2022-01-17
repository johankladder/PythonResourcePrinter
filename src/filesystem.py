import os


class FileSystem:

    @staticmethod
    def generate_file_path(queue_item_id: int) -> str:
        return os.path.join("documents/queue-item-" + str(queue_item_id) + ".pdf")

    @staticmethod
    def write_file(path: str, file_bytes):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f = open(path, 'wb')
        f.write(file_bytes)
        f.close()

    @staticmethod
    def remove_file(path: str):
        if os.path.isfile(path):
            os.remove(path)

