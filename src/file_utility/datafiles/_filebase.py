# -*- coding=utf-8 -*-
r"""

"""
import weakref
import os
import logging

MISSING = object()
INIT_PLACEHOLDER = lambda *a, **kw: None  # noqa

INSTANCEREGISTRY = weakref.WeakValueDictionary()


class FileBase(object):
    __stamp = None  # check-value if the real file has changed
    _filepath: str
    
    # creation #########################################################################################################
    
    def __init_subclass__(cls, **kwargs):
        logging.info('new class is registered: {}'.format(cls))
        # __init__ is moved because this class can return the same object on instantiation
        # this way __init__ is only explicit called
        cls.__real_init__ = cls.__init__  # noqa
        cls.__init__ = INIT_PLACEHOLDER
    
    def __new__(cls, *args, **kwargs):
        try:
            fp = kwargs['fp']
        except KeyError:
            try:
                fp = kwargs['filepath']
            except KeyError:
                if len(args) > 0:
                    fp = args[0]
                else:
                    raise KeyError('missing filepath argument')
        fp = os.path.abspath(fp)
        logging.debug('create/load instance for <{}>'.format(fp))
        
        try:
            return INSTANCEREGISTRY[fp]  # try to load
        except KeyError:  # or create new
            obj = super().__new__(cls)
            obj.__real_init__(*args, **kwargs)  # noqa
            obj.file_has_changed()  # update information / init-call
            INSTANCEREGISTRY[fp] = obj
            return obj
    
    # code management ##################################################################################################
    
    def __repr__(self):
        return '<{}.{} - {}>'.format(self.__class__.__module__, self.__class__.__qualname__, id(self))
    
    def __enter__(self):
        raise NotImplementedError()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()
    
    # data management ##################################################################################################
    
    def file_has_changed(self) -> bool:
        r"""
        return True if the file has changed. Otherwise False
        """
        stamp = os.path.getmtime(self._filepath)  # ?same as os.stat but faster?
        # stamp = os.stat(self._filepath).st_mtime
        if stamp != self.__stamp:
            self.__stamp = stamp
            return True
        return False
