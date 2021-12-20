# -*- coding=utf-8 -*-
r"""

"""
from ._filebase import FileBase
import configparser


class IniFile(FileBase):
    def __init__(self, fp: str, context_restore: bool = True, context_save: bool = True):
        self._filepath = fp
        self._context_restore = context_restore
        self._context_save = context_save

    def __enter__(self):
        if self._context_restore:
            self._backup = self.data  # self.data => copy | self._data => original
        return self  # don't know if this is more useful than useless

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val, exc_tb)):  # exception within with-statement
            if self._context_restore:
                self._data = self._backup
                del self._backup
        else:
            if self._context_save:
                self.save()

    ####################################################################################################################
    
    def __getitem__(self, item):
        section, key = item
    
    def get(self, section: str, key: str, default=None):
        try:
            return self.__getitem__((section, key))
        except KeyError:
            return default
    
    def __setitem__(self, item, value):
        section, key = item
    
    def set(self, section: str, key: str, value):
        self.__setitem__((section, key), value)
        
    def __delitem__(self, item):
        section, key = item
    
    def delete(self, section: str, key: str):
        self.__delitem__((section, key))
    
    ####################################################################################################################
    
    def reload(self):
        pass
    
    def save(self):
        pass
