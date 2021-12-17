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

"""
from ._filebase import FileBase
from .jsonfile import JsonFile
