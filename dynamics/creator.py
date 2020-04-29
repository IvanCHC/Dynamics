"""The module `dynamics.creator` is a meta-factory which create classes that
for nonlinear dynamics simulation. 
"""

import array
import copy
import warnings

class_replacers = {}

def create(name, base, **kwargs):
    """Creates a new class with a given *name* and inheriting from *base* in
    this module `dynamics.creator`. The new class can have attributes defined
    by the keyword argument(s).

    Parameters:
        name (str): Name of the created class.
        base (class): Parent class.
        attribure (~): Attribute(s) of the created class.
    """

    if name in globals():
        warnings.warn("Class '{0}' has already been created and it will be "
                      "overwritten.".format(name), RuntimeWarning)
    
    dict_inst = {}
    dict_cls = {}
    for key, value in kwargs.items():
        if isinstance(value, type):
            dict_inst[key] = value
        else:
            dict_cls[key] = value

    # Check if the base class has to be replaced
    if base in class_replacers:
        base = class_replacers[base]

    def initType(self, *args, **kwargs):
        """New init type which allows adding attributes form **kwargs to the
        instatnce."""
        for key, value in dict_inst.items():
            setattr(self, key, value())
        if base.__init__ is not object.__init__:
            base.__init__(self, *args, **kwargs)

    objtype = type(str(name), (base,), dict_cls)
    objtype.__init__ = initType
    global()[name] = objtype

    return objtype()
    