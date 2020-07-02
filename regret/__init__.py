try:
    from importlib import metadata
except ImportError:  # pragma: no cover
    import importlib_metadata as metadata

from regret._api import _DEPRECATOR, Deprecator, EmittedDeprecation


__version__ = metadata.version("regret")
callable = _DEPRECATOR.callable
inheritance = _DEPRECATOR.inheritance
