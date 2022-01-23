# -*- coding=utf-8 -*-
r"""

"""
import os
import sys

from .filestats import FileStats


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
    
    mode = mode.lower()
    
    import re
    match: re.Match = re.fullmatch(r'(u?g?o?a?)([+\-=])(r?w?x?)', mode)
    if not match:
        raise ValueError('invalid mode: {!r}'.format(mode))

    users_characters = match.group(1)
    update_mode = match.group(2)
    permissions_characters = match.group(3)
    
    if 'a' in users_characters:
        users_characters = 'ugo'
    
    import stat
    
    old_filemode = stat.S_IMODE(os.stat(path).st_mode)
    # original-...
    newuser = old_filemode % 8
    newgroup = (old_filemode // 8) % 8
    newother = (old_filemode // 8 // 8) % 8
    
    # todo
    
    os.chmod(path, int('0o{}{}{}'.format(newuser, newgroup, newother), base=8))


if sys.platform == "win32":
    def hide_file(path: str, hidden: bool):
        r"""
        mark file as hidden
        """
        # https://docs.microsoft.com/de-de/windows/win32/api/fileapi/nf-fileapi-setfileattributesa?redirectedfrom=MSDN
        import ctypes
        import stat
        if hidden:
            attribute = stat.FILE_ATTRIBUTE_HIDDEN
        else:
            attribute = stat.FILE_ATTRIBUTE_NORMAL
        ctypes.windll.kernel32.SetFileAttributesW(path, attribute)
