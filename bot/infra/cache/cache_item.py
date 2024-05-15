import time


class CacheItem:
    def __init__(self, data):
        self.data = data
        self.admitted_timestamp = time.time()
        self.__dirty = False

    def is_dirty(self) -> bool:
        return self.__dirty

    def set_dirty(self):
        self.__dirty = True

    def __eq__(self, other) -> bool:
        if not isinstance(other, CacheItem):
            return False
        return self.data == other.data

    def __hash__(self):
        return hash(self.data)
