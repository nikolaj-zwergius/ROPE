from typing import Any


class RangeDict(dict):
    """Map integer positions to values stored under range keys.

    Integer assignments are normalized to one-element ranges. An integer
    lookup returns the first stored range containing it, while a range lookup
    requires an exact stored key. Range membership is true when any position
    in the queried range is covered; consequently, setting an overlapping key
    is ignored rather than replacing or splitting existing ranges.
    """

    def __setitem__(self, key: int | range, value: Any) -> None:
        if key in self:
            return
        if not isinstance(key, range):
            super().__setitem__(range(key,key+1), value)
        else:
            super().__setitem__(key, value)

    def __contains__(self, item: int | range) -> bool:
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

    def __getitem__(self, item: int | range) -> Any:
        if not isinstance(item, range): # or xrange in Python 2
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)
        
    def override(self, key: int | range, value: Any) -> None:
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