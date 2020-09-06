#!/usr/bin/env python

from pyre.units import parser

parser = parser()

def test1():
    one_meter = parser.parse('1.*meter')
    assert(one_meter / parser.parse('1.*cm')==100.)
    return

def main():
    test1()
    return

if __name__ == '__main__': main()
