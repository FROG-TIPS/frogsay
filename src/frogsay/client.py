import contextlib
import random

import six
import semidbm
from RIBBIT.client import RIBBITClient


str = six.text_type


@contextlib.contextmanager
def open_client(cache_dir):
    """\
    Open and return a FROG tips client backed by a cache.
    """
    with Cache(cache_dir) as cache:
        yield Client(cache)


class Cache(object):
    """\
    This is a more Pythonic wrapper around shelve's open/close functions.
    """
    def __init__(self, cache_dir):
        self._cache_dir = cache_dir
        self._cache = None

    def __enter__(self):
        self._cache = semidbm.open(self._cache_dir, flag='c')
        return self._cache

    def __exit__(self, *ex_info):
        self._cache.close(compact=True)


class Client(object):
    """\
    This client wraps RIBBIT's FROG tips client and returns FROG tips either
    from a cache or from the client when the cache is empty.
    """

    def __init__(self, cache):
        self._client = RIBBITClient()
        self._cache = cache

    @property
    def should_refresh(self):
        return len(self._cache.keys()) == 0

    @property
    def num_cached_tips(self):
        return len(self._cache.keys())

    def frog_tip(self):
        """\
        Return a single FROG tip.
        """
        cache = self._cache
        client = self._client

        if self.should_refresh:
            tips = client.croak()
            for number, tip in tips.items():
                cache[str(number)] = tip

        choice = random.choice(list(cache.keys()))

        # We'll get a bytes() object here during real usage
        # but a text-like object in the tests. Good job Python
        try:
            tip = cache[choice].decode()
        except AttributeError:
            tip = cache[choice]

        del cache[choice]

        return tip
