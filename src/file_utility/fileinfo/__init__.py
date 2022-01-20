# -*- coding=utf-8 -*-
r"""

"""
import os
import sys


def chmod(path: str, mode: str):
    r"""
    like os.chmod() but mode is passed like in command-line
    for example: +x u+r
    
    u = owner of the file
    g = group of the file
    o = other users
    a = owner, group and others
    """
    # https://wiki.ubuntuusers.de/chmod/
    raise NotImplementedError()
    
    import re
    match: re.Match = re.fullmatch(r'(u?g?o?a?)([+\-=])(r?w?x?)', mode)
    # match: re.Match = re.fullmatch(r'(?P<users>u?g?o?a?)(?P<mode>[+\-=])(?P<permissions>r?w?x?)', mode)
    if not match:
        raise ValueError('invalid mode: {!r}'.format(mode))
    
    users = match.group(1)
    mode = match.group(2)
    permissions = match.group(3)
    
    if 'a' in users:
        users = None
    
    mode_number = 0
    
    os.chmod(path, )


if sys.platform == "win32":
    def hide_file(path: str, hidden: bool):
        r"""
        mark file as hidden
        """
        # https://docs.microsoft.com/de-de/windows/win32/api/fileapi/nf-fileapi-setfileattributesa?redirectedfrom=MSDN
        import ctypes
        if hidden:
            attribute = 0x2  # FILE_ATTRIBUTE_HIDDEN
        else:
            attribute = 0x80  # FILE_ATTRIBUTE_NORMAL
        ctypes.windll.kernel32.SetFileAttributesW(path, attribute)
