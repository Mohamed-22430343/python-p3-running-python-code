from lib.testing.conftest import pytest_itemcollected

# python

class DummyObj:
    def __init__(self, doc=None, name="dummy"):
        self.__doc__ = doc
        self.__name__ = name
        self.__class__ = type("DummyClass", (), {})

class DummyItem:
    def __init__(self, par_doc=None, node_doc=None, par_name="Parent", node_name="func"):
        self.parent = type("Parent", (), {})()
        self.parent.obj = DummyObj(doc=par_doc, name=par_name)
        self.obj = DummyObj(doc=node_doc, name=node_name)
        self._nodeid = None

def test_sets_nodeid_with_docstrings():
    item = DummyItem(par_doc="Parent doc", node_doc="Node doc")
    pytest_itemcollected(item)
    assert item._nodeid == "Parent doc Node doc"

def test_sets_nodeid_with_fallback_names():
    item = DummyItem(par_doc=None, node_doc=None, par_name="ParentClass", node_name="test_func")
    pytest_itemcollected(item)
    # Should use class name for parent and function name for node
    assert item._nodeid == "DummyClass test_func"

def test_sets_nodeid_with_partial_docstrings():
    item = DummyItem(par_doc="Parent doc", node_doc=None, node_name="test_func")
    pytest_itemcollected(item)
    assert item._nodeid == "Parent doc test_func"

    item2 = DummyItem(par_doc=None, node_doc="Node doc", par_name="ParentClass")
    pytest_itemcollected(item2)
    assert item2._nodeid == "DummyClass Node doc"

def test_nodeid_not_set_if_both_missing():
    item = DummyItem(par_doc=None, node_doc=None, par_name="", node_name="")
    pytest_itemcollected(item)
    assert item._nodeid == "DummyClass "