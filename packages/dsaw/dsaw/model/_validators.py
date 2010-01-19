# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.inventory import less, lessEqual, greater, greaterEqual, range,\
     choice, isBoth, isEither, isNot


def positive(v):
    if v<=0: raise ValueError, 'must be positive'
    return v

def nonnegative(v):
    if v<0: raise ValueError, 'must be NOT negative'
    return v

def negative(v):
    if v>=0: raise ValueError, 'must be negative'
    return v

def nonpositive(v):
    if v>0: raise ValueError, 'must be NOT positive'
    return v


def notempty(s):
    if len(s)==0: raise ValueError, 'must be NOT empty'
    return s


def variablename(s):
    'make sure string s can be a varaible name'
    if not s: raise ValueError, 'must be not empty'
    import re
    p = re.compile('\A[a-z]\w*\Z')
    s1 = s.lower()
    if not p.match(s1): raise ValueError, "must be a valid varaible name that starts with an alphabet character, with no space and special characters. examples: a, a3, a_3, abc"
    return s


def range(low, high, brackets='[)'):
    leftb = brackets[0]
    rightb = brackets[1]
    left = {'[': '>=', '(': '>'}[leftb]
    right = {']': '<=', ')': '<'}[rightb]
    expr = 'x %s %s and x %s %s' % (left, low, right, high)

    left2 = {'[': '<=', '(': '<'}[leftb]
    view = '%s%s, %s%s' % (brackets[0], low, high, brackets[1])
    
    def f(x):
        if not eval(expr): raise ValueError, 'must be in the range %s' % view
        return x
    return f


# version
__id__ = "$Id$"

# End of file 
