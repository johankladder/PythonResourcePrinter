import os


class FileSystem:

    @staticmethod
    def write_file(path: str, file_bytes):
        f = open(path, 'wb')
        f.write(file_bytes)
        f.close()

    @staticmethod
    def remove_file(path: str):
        if os.path.isfile(path):
            os.remove(path)

