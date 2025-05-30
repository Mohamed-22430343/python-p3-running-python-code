#!/usr/bin/env python3

def pytest_itemcollected(item):
    """
    Customize the display name of each test in pytest by combining
    the parent and node docstrings or names.
    """
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
