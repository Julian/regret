import importlib_metadata

from regret._api import _DEPRECATOR, Deprecator, EmittedDeprecation


__version__ = importlib_metadata.version(__name__)
callable = _DEPRECATOR.callable
