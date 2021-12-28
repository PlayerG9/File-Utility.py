# -*- coding=utf-8 -*-
r"""

"""
from ..datafiles import JsonFile as NormalJsonFile


class SyncedJsonFile(NormalJsonFile):
    r"""
    same as file_utility.datafile.JsonFile
    but automatically reloads the data from the file if the file-contents have changed.
    Also, automatically saves the changes to the file.
    
    if this file is used as context, the changes get only saved after the context exits
    if an exception occures during the context the data is restored to the state before the context
    
    if you want to make many changes, use the context because it's faster, because then this object doesn't save
    each change individually to the file
    """
    __context: bool
    
    def __init__(self, fp: str, load_config: dict = None, save_config: dict = None):
        super().__init__(fp=fp, load_config=load_config, save_config=save_config,
                         context_restore=True,  context_save=True)
    
    def __enter__(self):
        super().__enter__()
        self.__context = True
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__context = False
        super().__exit__(exc_type, exc_val, exc_tb)
    
    def __getitem__(self, path):
        if self.__context:
            return super().__getitem__(path)
        else:
            if self.file_has_changed():
                self.reload()
            return super().__getitem__(path)
    
    def __setitem__(self, key, value):
        if self.__context:
            super().__setitem__(key, value)
        else:
            if self.file_has_changed():
                self.reload()
            super().__setitem__(key, value)
            self.save()
    
    def __delitem__(self, path):
        if self.__context:
            super().__delitem__(path)
        else:
            if self.file_has_changed():
                self.reload()
            super().__delitem__(path)
            self.save()
