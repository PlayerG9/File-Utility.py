# -*- coding=utf-8 -*-
r"""

"""
from ._filebase import FileBase, MISSING
from copy import deepcopy
import json


class JsonFile(FileBase):
    r"""
    represents a json-file
    you get the same object for each same fp parameter
    
    a = JsonFile('file.json')
    b = JsonFile('file.json')
    print(a is b)  # => True
    """
    
    def __init__(self, fp: str, load_config: dict = None, save_config: dict = None,
                 context_restore: bool = True, context_save: bool = True):
        r"""
        represent a json-file
        
        :param fp: path to the json file
        :param load_config: passed to json.load
        :param save_config: passed to json.dump
        :param context_restore: if true the data is restored to the state before context if an exception occures
        :param context_save: if true the data is automatically saved to the file after context (only without exception)
        """
        self._filepath = fp
        self._data: dict = {}
        self._backup: dict  # exists only in a with-statement | maybe replace with stack for multiple with-statements
        self._load_config = load_config or {}  # passed to json.load
        self._save_config = save_config or {}  # passed to json.dump
        self._context_restore = context_restore
        self._context_save = context_save
        self.reload()
    
    def __enter__(self):
        if self._context_restore:
            self._backup = self.data  # self.data => copy | self._data => original
        return self  # don't know if this is more useful than usless
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if any((exc_type, exc_val, exc_tb)):  # exception within with-statement
            if self._context_restore:
                self._data = self._backup
                del self._backup
        else:
            if self._context_save:
                self.save()
    
    ####################################################################################################################
    
    @property
    def data(self) -> dict:
        # returns a copy if the data
        return deepcopy(self._data)
    
    ####################################################################################################################
    
    def __getitem__(self, *path):
        r"""
        maybe this should return a copy of the requested data in case the returned data gets modified (list, dict)
        """
        pass
    
    def get(self, *path, default=MISSING):
        r"""
        query a value from the json
        
        :param path: strings/keys
        :param default: return-value if item is not found
        :return:
        """
        try:
            return self.__getitem__(*path)
        except KeyError:
            return default
    
    # def __setitem__(self, *path, value):  # should be but now possible
    def __setitem__(self, *path):
        r"""
        maybe this should set a copy of the value in case the passed object gets modified (list, dict)
        """
        path, value = path[:-1], path[-1]
    
    def set(self, *path):
        r"""
        set a value
        
        :param path: strings/keys
        :return:
        """
        self.__setitem__(*path)
    
    def __delitem__(self, *path):
        pass
    
    def delete(self, *path):
        r"""
        delete something from the json
        
        :param path: strings/keys
        :return:
        """
        self.__delitem__(*path)
    
    ####################################################################################################################
    
    def reload(self):
        r"""
        if you want to undo your changes the file can be reloaded
        """
        with open(self._filepath) as jsonfile:
            self._data = json.load(jsonfile, **self._load_config)
    
    def save(self):
        r"""
        if you want to save your changes to the file
        """
        with open(self._filepath) as jsonfile:
            json.dump(self._data, jsonfile, **self._save_config)
