import contextlib
import os
import time
import random
import shutil


@contextlib.contextmanager
def temp_dir_name(mode='w+b', build_dir='../build'):
    slug = '{0}.{1}'.format(str(time.time()), random.random())
    name = os.path.join(os.path.abspath(build_dir), slug)
    yield name
    shutil.rmtree(name)
