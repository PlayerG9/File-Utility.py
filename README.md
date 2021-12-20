# File-Utility.py
 simple and advanced file utilitys for python

# help is appriciated
- if you have found bugs for this package
  - [create a ticket](https://github.com/PlayerG9/File-Utility.py/issues/new/choose)
- if you have ideas for this package
  - [create a ticket](https://github.com/PlayerG9/File-Utility.py/issues/new/choose)
- if you want to make own changes
  - [create a pull request](https://github.com/PlayerG9/File-Utility.py/pulls)

-----

# Examples
here are some example usages

- [Resources](#resources)
- [DataFiles](#datafiles)

This is the project structure for the examples
```text
project/
├─ files/
│  ├─ config.json
│  ├─ icon.png
├─ some_functions/
│  ├─ __init__.py
├─ main.py
```

## Resources
how to manage resources like config-files or images

`project/main.py`
```python
import some_functions
```

`project/some_functions/__init__.py`
```python
from file_utility.resources import resource

print(resource('files', 'config.json'))  # 'project/files/config.json
```

`output/console`
```commandline
$ python3 main.py
project/files/config.json
```

## DataFiles
how to manage configurations over your script
(in this case json)

`project/main.py`
```python
import some_functions
```

`project/some_functions/__init__.py`
```python
from file_utility.datafiles import JsonFile
from file_utility.resources import resource

config_file = resource('files', 'config.json')

a = JsonFile(config_file)
b = JsonFile(config_file)

print("A = ", a['key'])  # 'value'
print("B = ", b['key'])  # 'value'

a['key'] = 'new'

print("A =", a['key'])  # 'new'
print("B =", b['key'])  # 'new'

print("A is B =", a is b)  # True
```

`output/console`
```commandline
$ python3 main.py
A = value
B = value
A = new
B = new
A is B = True
```
