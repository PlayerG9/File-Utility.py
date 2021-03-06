# -*- coding=utf-8 -*-
r"""
varius functions for project resources
"""
import functools
import os


class DynamicMainError(Exception):
    pass


def cached():
    return functools.lru_cache(maxsize=1)


def to_filename(name):
    """
    Convert a project or version name to its filename-escaped form

    Any '-' characters are currently replaced with '_'.
    """
    return name.replace('-', '_')


@cached()
def scriptdir() -> str:
    r"""
    get the directory of the executed script (__main__)
    
    same as `os.path.dirname(__file__)` executed in `main.py` but callable from every file
    """
    import sys
    __main__ = sys.modules['__main__']
    if not hasattr(__main__, '__file__'):
        raise DynamicMainError('main-script was created dynamically or run as interactive shell')
    return os.path.abspath(os.path.dirname(__main__.__file__))


def resource(*path) -> str:
    r"""
    get a resource in the directory of the executed script (__main__)
    
    this is helpful if you change the working-directory (os.chdir())
    or try to access resources (like images) from a different file than main
    
    resource('images', 'config.json') => '.../project/images/config.json'
    project/
    ├─ images/
    │  ├─ config.json          <= access this
    ├─ some_functions/
    │  ├─ __init__.py          <= from here
    ├─ main.py
    
    same as `os.path.join(scriptdir(), ...)`
    """
    return os.path.join(scriptdir(), *path)
