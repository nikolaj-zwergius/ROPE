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
            for element in item:
                if self.__contains__(element):
                    return True
            return False

    def __getitem__(self, item):
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)
        
    def override(self, key, value):
        if not isinstance(key,range):
            if not super().__contains__(range(key,key+1)):
                raise Exception("""override can only be used if a excat key is given, for other use cases remove overlapping element first
                            before adding the new one""")
        elif not super().__contains__(key):
            raise Exception("""override can only be used if a excat key is given, for other use cases remove overlapping element first
                            before adding the new one""")

        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)