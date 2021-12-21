# -*- coding=utf-8 -*-
r"""

"""
from ._filebase import FileBase
import os
import io
import pickle


MAGIC_NUMBER = b'PyObj'


class PyObjFile(FileBase):
    def __init__(self, fp: str):
        self._filepath = fp
        if not self._number_check():
            raise OSError("invalid file-content")
    
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
        with open(self.filepath, 'rb') as file:
            file: io.BufferedIOBase
            self._jump_to(file, index)  # go to index
            bytes_size = self._read_bsize(file)
            object_bytes = file.read(bytes_size)  # read the size
            return pickle.loads(object_bytes)  # convert back / load object

    def add(self, value) -> int:
        with open(self.filepath, 'rb') as file:
            pass
    
    def delete(self, index: int = None):
        with open(self.filepath, 'ab'):  # does this clear the file
            pass
    
    def delete_many(self, indezies: list):
        pass

    ####################################################################################################################
    
    def size(self) -> int:
        pass
    
    ####################################################################################################################
    
    def _number_check(self):
        with open(self.filepath, 'rb') as file:
            return file.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER
    
    @staticmethod
    def _jump_to(file: io.BufferedIOBase, index: int):
        if file.read(len(MAGIC_NUMBER)) != MAGIC_NUMBER:
            raise OSError('invalid file-content')
        pass
    
    @staticmethod
    def _read_bsize(file) -> int:
        size_bytes = file.read(2)  # read 2 bytes (constant size)
        return int.from_bytes(size_bytes, 'little', signed=True)  # convert bytes to integer
