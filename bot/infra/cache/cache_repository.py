import copy
from threading import RLock
from typing import Dict, Callable

from bot.infra.cache.cache_item import CacheItem
from bot.infra.cache.exception.cache_find_operation_not_found_exception import (
    CacheFindOperationNotFoundException,
)
from bot.infra.cache.exception.cache_item_not_found_exception import (
    CacheItemNotFoundException,
)


class CacheRepository:
    MAX_ITEMS = 10

    def __init__(self):
        self.__cache: Dict[any, CacheItem] = {}
        self.__lock = RLock()

    def __remove_older_item(self):
        oldest_key = min(self.__cache, key=lambda k: self.__cache[k].admitted_timestamp)
        self.__cache.pop(oldest_key)

    def _remove_cached_item(self, cache_id):
        if self._is_cached(cache_id):
            del self.__cache[cache_id]

    def _is_cached(self, cache_id) -> bool:
        return cache_id in self.__cache

    def _is_dirty(self, cache_id) -> bool:
        return self.__cache[cache_id].is_dirty()

    def _get_cached_item(self, cache_id: any) -> CacheItem:
        try:
            return copy.deepcopy(self.__cache[cache_id])
        except (ValueError, KeyError):
            raise CacheItemNotFoundException(cache_id)

    def _set_dirty(self, cache_id):
        if self._is_cached(cache_id):
            with self.__lock:
                self.__cache[cache_id].set_dirty()

    def _set_cached_item(self, cache_id, data):
        if not self._is_cached(cache_id) and len(self.__cache) + 1 > self.MAX_ITEMS:
            with self.__lock:
                self.__remove_older_item()

            self.__cache[cache_id] = CacheItem(data)

    def _find_cache_item(self, predicate: Callable[[CacheItem], bool]):
        for cache_id, cache_object in self.__cache.items():
            cache_id: any
            cache_object: CacheItem
            if (
                self._is_cached(cache_id)
                and not self._is_dirty(cache_id)
                and predicate(cache_object)
            ):
                return self._get_cached_item(cache_id).data
        raise CacheFindOperationNotFoundException()
