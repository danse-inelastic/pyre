#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# factories
def facility(name, **kwds):
    from Facility import Facility
    return Facility(name, **kwds)


def curator(name):
    from odb.Curator import Curator
    return Curator(name)


def registry(name):
    from odb.Inventory import Inventory
    return Inventory(name)


# persistence
def codecPML():
    from pml.CodecPML import CodecPML
    return CodecPML()


def renderer(mode="pml"):
    if mode == "pml":
        from pml.Renderer import Renderer
        return Renderer()

    import journal
    journal.error.log("'%s': unknown registry rendering mode" % mode)
    return None
    

def parser(mode="pml"):
    if mode == "pml":
        from pml.Parser import Parser
        return Parser()

    import journal
    journal.error.log("'%s': unknown registry parsing mode" % mode)
    return None
    

# builtin property types
def array(name, **kwds):
    '''Create an inventory type for a list of floats.
    It can be initialized from a string of comma separated floats,
    that may be enclosed in parenthesis, brackets or braces.

    name    -- public name of this item, used on command line and
               PML files.

    Keyword arguments:

    default     -- default list of floats, when not specified use empty list.
    validator   -- function of one variable that returns its validated value
                   (usually the same) or raises ValueError

    Returns an instance of Array from inventory.properties.Array.
    Raises TypeError when assigned value that cannot be converted to
    a list of floats.

    Notable attributes of the returned type:

    meta    -- dictionary, where items ('tip', 'doc') provide short
               and long description of the inventory item.
    '''
    from properties.Array import Array
    return Array(name, **kwds)


def bool(name, **kwds):
    '''Create a boolean inventory type that is by default False.
    It can be assigned from case-insensitive strings of
    (1, y, yes, on, t, true) or (0, n, no, off, f, false).

    name    -- public name of this item, used on command line and
               PML files.

    Keyword arguments:

    default     -- default boolean flag, can be None to indicate unassigned
                   variable
    validator   -- function of one variable that returns its validated value
                   (usually the same) or raises ValueError.

    Returns an instance of Bool from inventory.properties.Bool.
    Raises KeyError when assigned unrecognized string.

    Notable attributes of the returned type:

    meta    -- dictionary, where items ('tip', 'doc') provide short
               and long description of the inventory item.
    '''
    from properties.Bool import Bool
    return Bool(name, **kwds)


def dimensional(name, **kwds):
    '''Inventory type for one or more values in specified SI units.
    It must be initialized from an instance of a pyre unit, that can
    be obtained by importing from pyre.units.QUANTITY, for example:

    from pyre.units.mass import kg
    m = pyre.inventory.dimensional('m', default=3*kg)

    An instance of dimensional can be also assigned string, where value
    and units are explicitly multiplied, for example "42*km".  Dimensional
    supports addition and subtraction for values with compatible units.

    name    -- public name of this item, used on command line and
               PML files.

    Keyword arguments:

    default     -- the default value, which declares units and shape for the
                   dimensional.  The default must be a multiple of SI units
                   obtained from pyre.units.QUANTITY.  Use tuple or list
                   to declare dimensional array, e.g., default=(1*kg, 2*m).
                   A constructed dimensional can be only assigned values with
                   compatible size and units, this can be also a string of
                   comma separated values.  Without any default, dimensional,
                   in a way beating its purpose.

    validator   -- function of one variable that returns its validated value
                   (usually the same) or raises ValueError.

    Returns an instance of Dimensional from inventory.properties.Dimensional.
    Raises ValueError when assigned value with incompatible units or shape.
    Raises SyntaxError, for unknown units.

    Notable attributes of the returned type:

    meta    -- dictionary, where items ('tip', 'doc') provide short
               and long description of the inventory item.

    Notable attributes of instantiated type:

    value   -- float value with respect to base SI units.
    '''
    from properties.Dimensional import Dimensional
    return Dimensional(name, **kwds)


def float(name, **kwds):
    from properties.Float import Float
    return Float(name, **kwds)


def inputFile(name, **kwds):
    from properties.InputFile import InputFile
    return InputFile(name, **kwds)


def int(name, **kwds):
    from properties.Integer import Integer
    return Integer(name, **kwds)


def list(name, **kwds):
    from properties.List import List
    return List(name, **kwds)


def outputFile(name, **kwds):
    from properties.OutputFile import OutputFile
    return OutputFile(name, **kwds)


def preformatted(name, **kwds):
    from properties.Preformatted import Preformatted
    return Preformatted(name, **kwds)


def slice(name, **kwds):
    from properties.Slice import Slice
    return Slice(name, **kwds)


def str(name, **kwds):
    from properties.String import String
    return String(name, **kwds)


# bultin validators
def less(value):
    from validators.Less import Less
    return Less(value)


def lessEqual(value):
    from validators.LessEqual import LessEqual
    return LessEqual(value)


def greater(value):
    from validators.Greater import Greater
    return Greater(value)


def greaterEqual(value):
    from validators.GreaterEqual import GreaterEqual
    return GreaterEqual(value)


def range(low, high):
    from validators.Range import Range
    return Range(low, high)


def choice(set):
    from validators.Choice import Choice
    return Choice(set)


# logical operators on validators
def isBoth(v1, v2):
    from validators.And import And
    return And(v1, v2)


def isEither(v1, v2):
    from validators.Or import Or
    return Or(v1, v2)


def isNot(v):
    from validators.Not import Not
    return Not(v)


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2006-11-27 00:10:01 aivazis Exp $"

# End of file 
