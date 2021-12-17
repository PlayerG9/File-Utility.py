# -*- coding=utf-8 -*-
r"""

"""
from ._filebase import FileBase, MISSING
from copy import deepcopy


class JsonFile(FileBase):
    def __init__(self, fp: str):
        self._filepath = fp
        self._data: dict = {}
        self._backup: dict  # exists only in a with-statement | maybe replace with stack for multiple with-statements
        self.reload()
    
    def __enter__(self):
        self._backup = self.data  # self.data => copy | self._data => original
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val, exc_tb)):  # exception within with-statement
            self._data = self._backup
            del self._backup
        self.save()

    ####################################################################################################################
    
    @property
    def data(self) -> dict:
        return deepcopy(self._data)
    
    ####################################################################################################################

    def __getitem__(self, *path):
        pass
    
    def get(self, *path, default=MISSING):
        try:
            return self.__getitem__(*path)
        except KeyError:
            return default
    
    def __setitem__(self, *path, value):
        pass
    
    def set(self, *path, value):
        self.__setitem__(*path, value=value)
    
    def __delitem__(self, *path):
        pass
    
    def delete(self, *path):
        self.__delitem__(*path)

    ####################################################################################################################
    
    def reload(self):
        pass
    
    def save(self):
        pass
