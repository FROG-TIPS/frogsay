from frogsay.client import open_client

from .util import temp_dir_name


def test_empty_cache_fetches_more_tips():
    with temp_dir_name() as db_dir:
        with open_client(db_dir) as client:
            # Exhaust all tips
            tries = 0
            max_tips = 49
            client.frog_tip()

            while not client.should_refresh:
                tries += 1
                client.frog_tip()

            assert tries == max_tips

        with open_client(db_dir) as client:
            assert client.num_cached_tips == 0
