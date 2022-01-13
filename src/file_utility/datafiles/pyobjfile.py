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
CHUNK_SIZE = 1024


class PyObjFile(FileBase):
    FILE_EXTENSION = '.pyobj'
    
    def __init__(self, fp: str):
        self._filepath = fp
        self._get_file().close()  # try to load file | check if content is valid
    
    def __enter__(self):
        raise NotImplementedError()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    ####################################################################################################################
    
    def __iter__(self):
        return iter_pyobjfile(self)

    ####################################################################################################################
    
    @classmethod
    def create_new(cls, filepath: str) -> 'PyObjFile':
        if os.path.isfile(filepath):
            raise FileExistsError("can't create file because it already exist")
        with open(filepath, 'wb') as file:
            file.write(MAGIC_NUMBER)
        return cls(filepath)

    ####################################################################################################################
    
    def __getitem__(self, index):
        with self._get_file() as file:
            file: io.BufferedIOBase
            self._jump_to(file, index)  # go to index
            object_size = self._read_bsize(file)  # get size of object
            object_bytes = file.read(object_size)  # read the size
            return pickle.loads(object_bytes)  # convert back / load object

    def get(self, index: int):
        return self[index]

    def add(self, *objects: object):
        with self._get_file() as file:
            file.seek(0, os.SEEK_END)  # go to the end
            for obj in objects:
                object_bytes = pickle.dumps(obj)  # dump object
                object_size = len(object_bytes)  # get size of object
                bytes_size = object_size.to_bytes(2, 'big', signed=False)  # convert size to bytes
                file.write(bytes_size)  # write size
                file.write(object_bytes)  # write object/bytes
    
    def delete(self, *indezies: int):
        r"""
        warning: .delete() with indezies is slow because it writes a new file
        thus it's reommended to gather the indezies that should be deleted and pass them at once
        """
        if not indezies:
            self.truncate()
            return
        
        tmpfile = self.filepath + '.tmp'
        
        index = 0
        
        with self._get_file() as old_file, open(tmpfile, 'wb') as new_file:  # open old and new files
            new_file.write(MAGIC_NUMBER)
            
            size_bytes = old_file.read(2)  # read size-bytes
            bytes_size = int.from_bytes(size_bytes, 'big', signed=False)  # parse object-size
            
            if index in indezies:  # should be deleted <=> ignored
                old_file.seek(old_file.tell() + bytes_size)  # skip
            else:
                new_file.write(size_bytes)  # write size
                chunk = old_file.read(CHUNK_SIZE)  # read (first) chunk
                while chunk:
                    new_file.write(chunk)  # write chunk
                    chunk = old_file.read(CHUNK_SIZE)  # next chunk
            
            index += 1
        
        os.replace(src=tmpfile, dst=self.filepath)  # replace old file and delete temp-file
    
    def truncate(self):
        r"""
        deletes all items from the file
        """
        with open(self.filepath, 'wb') as file:
            file.write(MAGIC_NUMBER)
    
    def insert(self, index: int, obj: object):
        raise NotImplementedError()  # todo
    
    def replace(self, index: int, obj):
        raise NotImplementedError()  # todo

    ####################################################################################################################
    
    def size(self) -> int:
        size = 0
        with self._get_file() as file:
            while True:
                try:
                    object_size = self._read_bsize(file)
                except EOFError:
                    break
                next_index = file.tell() + object_size
                file.seek(next_index)
                size += 1
        return size
    
    ####################################################################################################################
    
    def _get_file(self):
        file = open(self.filepath, 'r+b')  # read | binary | updating (reading and writing)
        if file.read(len(MAGIC_NUMBER)) != MAGIC_NUMBER:
            raise OSError('invalid file-content')
        return file
    
    def _jump_to(self, file: io.BufferedIOBase, index: int):
        file.seek(len(MAGIC_NUMBER))  # go to first
        for _ in range(index):
            object_size = self._read_bsize(file)
            next_index = file.tell() + object_size
            file.seek(next_index)
    
    @staticmethod
    def _read_bsize(file) -> int:
        size_bytes = file.read(2)  # read 2 bytes (constant size)
        if not size_bytes:
            raise EOFError()
        return int.from_bytes(size_bytes, 'big', signed=False)  # convert bytes to integer

########################################################################################################################


def iter_pyobjfile(pyobjfile: PyObjFile):
    with pyobjfile._get_file() as file:
        try:
            object_size = pyobjfile._read_bsize(file)
        except EOFError:
            raise StopIteration()
        object_bytes = file.read(object_size)
        yield pickle.loads(object_bytes)
