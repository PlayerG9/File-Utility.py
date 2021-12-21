# -*- coding=utf-8 -*-
r"""

"""
r"""
r | open for reading (default)
w | open for writing, truncating the file first
x | open for exclusive creation, failing if the file already exists
a | open for writing, appending to the end of file if it exists
b | binary mode
t | text mode (default)
+ | open for updating (reading and writing)
"""
from ._filebase import FileBase
import os
import io
import pickle


MAGIC_NUMBER = b'PyObj'


class PyObjFile(FileBase):
    def __init__(self, fp: str):
        self._filepath = fp
        self._get_file().close()  # try to load file | check if content is valid
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    ####################################################################################################################
    
    @staticmethod
    def create_empty_file(filepath: str):
        if os.path.isfile(filepath):
            raise FileExistsError("can't create file because it already exist")
        with open(filepath, 'wb') as file:
            file.write(MAGIC_NUMBER)

    ####################################################################################################################

    def get(self, index: int):
        with self._get_file() as file:
            file: io.BufferedIOBase
            self._jump_to(file, index)  # go to index
            bytes_size = self._read_bsize(file)
            object_bytes = file.read(bytes_size)  # read the size
            return pickle.loads(object_bytes)  # convert back / load object

    def add(self, value) -> int:
        with self._get_file() as file:
            pass
    
    def delete(self, index: int = None):
        with open(self.filepath, 'ab'):  # does this clear the file
            pass
    
    def delete_many(self, indezies: list):
        pass

    ####################################################################################################################
    
    def size(self) -> int:
        with self._get_file() as file:
            pass
    
    ####################################################################################################################
    
    def _get_file(self):
        file = open(self.filepath, 'r+b')  # read | binary | updating (reading and writing)
        if file.read(len(MAGIC_NUMBER)) != MAGIC_NUMBER:
            raise OSError('invalid file-content')
        return file
    
    @staticmethod
    def _jump_to(file: io.BufferedIOBase, index: int):
        pass
    
    @staticmethod
    def _read_bsize(file) -> int:
        size_bytes = file.read(2)  # read 2 bytes (constant size)
        return int.from_bytes(size_bytes, 'little', signed=True)  # convert bytes to integer
