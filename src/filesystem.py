import os


class FileSystem:

    def write_file(self, path: str, file_bytes):
        f = open(path, 'wb')
        f.write(file_bytes)
        f.close()

    def remove_file(self, path: str):
        if os.path.isfile(path):
            os.remove(path)

