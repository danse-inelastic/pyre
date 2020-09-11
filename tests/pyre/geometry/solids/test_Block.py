# -*- python -*-
# Jiao Lin <jiao.lin@gmail.com>

def testBlock():
    from pyre.geometry.solids.Block import Block
    block = Block((1,2,3))
    text = str(block)
    assert text == 'block: diagonal=(1, 2, 3)'
    return

if __name__ == '__main__': testBlock()
