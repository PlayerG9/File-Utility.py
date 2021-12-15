# -*- coding=utf-8 -*-
r"""
open files like .json .ini and more process-same

every time you open a file it's the same object

a = open_datafile('./data.json')
b = open_datafile('./data.json')

print(a['key'])  # 'value'
print(b['key'])  # 'value'

a['key'] = 'new'

print(a['key'])  # 'new'
print(b['key'])  # 'new'

print(a is b)  # True
"""
