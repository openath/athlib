"""Utilities for working with JSON and json-like structures - deeply nested
Python dicts and lists.

This lets us iterate over child nodes and access elements with a dot-notation.
"""


class MyLocals(object):
    pass


mylocals = MyLocals()


def setErrorCollect(collect):
    mylocals.error_collect = collect


setErrorCollect(False)


def errorValue(x):
    if isinstance(x, (str, unicode)):
        return repr(x) if ' ' in x else x

    return 'None' if x is None else str(x)


def condJSON(v, __name__=''):
    if isinstance(v, dict):
        return JSONDict(v, __name__=__name__)
    elif isinstance(v, list):
        return JSONList(v, __name__=__name__)
    else:
        return v


def condJSONSafe(v, __name__=''):
    if isinstance(v, dict):
        return JSONDictSafe(v, __name__=__name__)
    elif isinstance(v, list):
        return JSONListSafe(v, __name__=__name__)
    else:
        return v


class JSONListIter(object):
    def __init__(self, lst, conv):
        self.lst = lst
        self.i = -1
        self.conv = conv

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self.lst) - 1:
            self.i += 1
            return self.conv(self.lst[self.i])
        else:
            raise StopIteration


class JSONList(list):
    def __init__(self, v, __name__=''):
        list.__init__(self, v)
        self.__name__ = __name__

    def __getitem__(self, x):
        return condJSON(list.__getitem__(self, x),
                        __name__='%s\t%s' % (self.__name__, errorValue(x)))

    def __iter__(self):
        return JSONListIter(self, condJSON)


class JSONListSafe(JSONList):
    def __getitem__(self, x):
        __name__ = '%s\t%s' % (self.__name__, errorValue(x))

        try:
            return condJSONSafe(list.__getitem__(self, x), __name__=__name__)
        except KeyError:
            if mylocals.error_collect:
                mylocals.error_collect(__name__)

            return JSONStrSafe('')

    def __iter__(self):
        return JSONListIter(self, condJSONSafe)


class JSONStrSafe(str):
    def __getattr__(self, attr):
        return self

    __getitem__ = __getattr__


class JSONDict(dict):
    "Allows dotted access"
    def __new__(cls, v={}, __name__=''):
        self = dict.__new__(cls, v)
        self.__name__ = __name__
        return self

    def __getattr__(self, attr, default=None):
        if attr in self:
            return condJSON(self[attr],
                            __name__='%s\t%s' % (self.__name__,
                                                 errorValue(attr)))
        elif unicode(attr) in self:
            return condJSON(self[unicode(attr)],
                            __name__='%s\t%s' % (self.__name__,
                                                 errorValue(attr)))
        elif attr == '__safe__':
            return JSONDictSafe(self, __name__=self.__name__)
        else:
            raise AttributeError("No attribute or key named '%s'" % attr)

    def sorted_items(self):
        return sorted([(k, condJSON(v)) for k, v in self.iteritems()])

    def sorted_keys(self):
        return sorted(self.keys())


class JSONDictSafe(JSONDict):
    "Allows dotted access"
    def __getattr__(self, attr, default=None):
        if attr in self:
            return condJSONSafe(self[attr],
                                __name__='%s\t%s' % (self.__name__,
                                                     errorValue(attr)))
        elif unicode(attr) in self:
            return condJSONSafe(self[unicode(attr)],
                                __name__='%s\t%s' % (self.__name__,
                                                     errorValue(attr)))
        elif attr == '__safe__':
            return self
        else:
            return JSONStrSafe('')

    def __getitem__(self, x):
        __name__ = '%s\t%s' % (self.__name__, errorValue(x))

        try:
            return condJSONSafe(dict.__getitem__(self, x), __name__=__name__)
        except KeyError:
            if mylocals.error_collect:
                mylocals.error_collect(__name__)

            return JSONStrSafe('')

    def sorted_items(self):
        return sorted([(k, condJSONSafe(v)) for k, v in self.iteritems()])
