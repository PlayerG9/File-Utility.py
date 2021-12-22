# -*- coding=utf-8 -*-
r"""
key(str)-value(str) database-files

https://docs.python.org/3/library/dbm.html
"""
from ._filebase import FileBase
import dbm
from typing import Union


_T = Union[str, bytes]


class DBFile(FileBase):
    FILE_EXTENSION = '.dbm'
    
    READY_ONLY = 'r'            # only read from file
    WRITE_AND_READ = 'w'        # read and write
    CREATE_IF_NOT_EXISTS = 'c'  # read and write (and create if not exists
    ALWAYS_NEW = 'n'            # ready and write and clear database-file
    
    def __init__(self, fp: str, mode: str = WRITE_AND_READ):
        self._filepath = fp
        self._file = dbm.open(fp, mode)  # noqa
    
    def __del__(self):
        self._file.close()
    
    def __enter__(self):
        self._file.__enter__()
        return self  # don't know if this is more useful than useless
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.__exit__(exc_type, exc_val, exc_tb)
    
    ####################################################################################################################
    
    def __getitem__(self, key: _T) -> bytes:
        return self._file[key]
    
    def get(self, key: _T, default=None) -> bytes:
        return self._file.get(key, default)
    
    def __setitem__(self, key: _T, value: _T):
        self._file[key] = value
    
    def set(self, key: _T, value: _T):
        self.__setitem__(key, value)
        
    def __delitem__(self, key: _T):
        del self._file[key]
    
    def delete(self, key: _T):
        del self._file[key]
