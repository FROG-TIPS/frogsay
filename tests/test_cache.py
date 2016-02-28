from nose.tools import raises

from frogsay.client import Cache
from .util import temp_dir_name


def test_actually_closes():
    with temp_dir_name() as db_dir:
        with Cache(db_dir) as cache:
            pass

        db_name = cache._data_filename

        with open(db_name, 'rb') as file:
            file.read()


def test_cache_opens_with_a_contextmanager_like_guido_intended():
    key = '1'
    value = 'DO NOT CACHE FROG.'

    with temp_dir_name() as db_dir:
        with Cache(db_dir) as cache:
            cache[key] = value

        with Cache(db_dir) as cache:
            assert cache[key].decode() == value


@raises(KeyError)
def test_cache_can_delete():
    key = '1'
    value = 'DO NOT DELETE FROG.'

    with temp_dir_name() as db_dir:
        with Cache(db_dir) as cache:
            cache[key] = value

        with Cache(db_dir) as cache:
            del cache[key]

        with Cache(db_dir) as cache:
            cache[key]
