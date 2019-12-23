try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

from regret._api import _DEPRECATOR, Deprecator, EmittedDeprecation


__version__ = metadata.version("regret")
callable = _DEPRECATOR.callable
