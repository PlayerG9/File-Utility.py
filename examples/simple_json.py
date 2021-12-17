# -*- coding=utf-8 -*-
r"""

"""
from file_utility.datafiles import JsonFile


a = JsonFile('./example-data/test.json')
b = JsonFile('./example-data/test.json')

print("A =", a['key'])  # 'value'
print("B =", b['key'])  # 'value'

a['key'] = 'new'

print("A =", a['key'])  # 'new'
print("B =", b['key'])  # 'new'

print("A is B =", a is b)  # True
