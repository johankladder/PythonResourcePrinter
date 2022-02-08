import os
from os import listdir
from os.path import isfile, join


class FileSystem:

    @staticmethod
    def get_documents_dir() -> str:
        return os.getcwd() + "/documents"

    @staticmethod
    def get_dir_prefix() -> str:
        return FileSystem.get_documents_dir() + "/queue-item-"

    @staticmethod
    def generate_file_path(queue_item_id: int) -> str:
        return os.path.join(FileSystem.get_dir_prefix() + str(queue_item_id) + ".pdf")

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

    @staticmethod
    def remove_files(paths: [str]):
        for path in paths:
            FileSystem.remove_file(path)

    @staticmethod
    def get_all_filepaths(path: str):
        return [path + "/" + f for f in listdir(path) if isfile(join(path, f))]
