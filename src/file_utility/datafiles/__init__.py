# -*- coding=utf-8 -*-
r"""
open files like .json .ini and more process-same

every time you open a file it's the same object


code example

>>> a = JsonFile('./example-data/test.json')
>>> b = JsonFile('./example-data/test.json')
>>>
>>> print("A = ", a['key'])  # 'value'
>>> print("B = ", b['key'])  # 'value'
>>>
>>> a['key'] = 'new'
>>>
>>> print("A =", a['key'])  # 'new'
>>> print("B =", b['key'])  # 'new'
>>>
>>> print("A is B =", a is b)  # True

planned/supported filetypes
| ext     | Class       | python-module |
+---------+-------------+---------------+
| .json   | JsonFile    | json          |
| .ini    | IniFile     | configparser  |
| .db     | DBFile      | dbm           |
| .pyobj  | PyObjFile | pickle        |
"""
from ._filebase import FileBase
from .jsonfile import JsonFile
from .inifile import IniFile
from .dbfile import DBFile
