import importlib
from glob import glob
from os.path import dirname, abspath, basename, join

__all__ = ['init_app']

CURRENT_DIR = abspath(dirname(__file__))


def init_app(app):
    py_files = glob(join(CURRENT_DIR, '*_controller.py')) + \
               glob(join(CURRENT_DIR, '*_controller.pye'))
    for f in py_files:
        fname = '.'.join(basename(f).split('.')[:-1])
        if fname == '__init__':
            continue
        module = import_module(fname)
        if module is not None and hasattr(module, 'app'):
            app.register_blueprint(module.app)


def import_module(name):
    return importlib.import_module('.' + name, package=__name__)
