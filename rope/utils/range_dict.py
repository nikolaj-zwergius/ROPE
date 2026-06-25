class RangeDict(dict):

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key {key} overlaps with existing key(s) in RangeDict.")
        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)

    def __contains__(self, item):
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return True
            return False
        else:
            return super().__contains__(item)

    def __getitem__(self, item):
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)
    def override(self, key, value):
        if key not in self:
            self.__setitem__(key, value)
        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)