# -*- coding=utf-8 -*-
r"""

"""
import os
import sys
import stat
from datetime import datetime

IS_UNIX = sys.platform != 'win32'


class FileStats:
    def __init__(self, fp: str):
        self._stat = os.stat(fp)
    
    def __repr__(self):
        return '<{} - {}>'.format(self.__class__, self._stat)
    
    @classmethod
    def from_os_stat(cls, stat_result: os.stat_result):
        new = cls.__new__(cls)
        new._stat = stat_result
        return new

    ####################################################################################################################
    
    @property
    def filemode(self):
        return stat.S_IMODE(self._stat.st_mode)
    
    @property
    def parsed_filemode(self) -> tuple:
        mode = self.filemode
        a = mode % 8
        b = (mode // 8) % 8
        c = (mode // 8 // 8) % 8
        return a, b, c
    
    ####################################################################################################################
    
    @property
    def fileowner_id(self):
        return self._stat.st_uid
    
    if IS_UNIX:
        @property
        def fileowner_name(self):
            from pwd import getpwuid
            return getpwuid(self._stat.st_uid).pw_name
    
    @property
    def group_id(self):
        return self._stat.st_gid
    
    if IS_UNIX:
        @property
        def group_name(self):
            from grp import getgrgid
            return getgrgid(self._stat.st_gid).gr_name

    ####################################################################################################################
    
    @property
    def create_at(self) -> datetime:
        # maybe self._stat.st_birthtime
        return datetime.fromtimestamp(self._stat.st_ctime)

    @property
    def last_access(self) -> datetime:
        return datetime.fromtimestamp(self._stat.st_atime)
    
    @property
    def last_modification(self) -> datetime:
        return datetime.fromtimestamp(self._stat.st_mtime)
