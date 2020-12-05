"""
A sample module that is deprecated and has no replacement.

The docstring of this module will go crazy as we deprecate it multiple times.
"""
import regret
import os
from datetime import date

# The most simple deprecations.
regret.module(version='1.2.0')

# A replacement that is a module instance.
regret.module(version='1.2.0', replacement=os.path)

# A replacement that is just string.
regret.module(version='1.2.0', replacement='some.other.module')

# We have a deprecate date.
regret.module(version='1.2.0', replacement=os.path, removal_date=date.today())

# Also with some extra info.
regret.module(version='1.2.0', replacement=os.path, addendum='Some info.')
