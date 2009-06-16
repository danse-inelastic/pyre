#!/usr/bin/env python

"""
>>> def preprocess(s):
...     return str(BeautifulSoup(s, convertEntities='html'))
...
>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''some <em>italic text</em> and some
... <b>bold text</b>.'''
>>> parser.feed(preprocess(s))
>>> parser.close()
>>> print writer.getvalue()
some *italic text* and some **bold text**.
<BLANKLINE>

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<h1>Header One</h1>'
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
Header One
==========
<BLANKLINE>


>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<h2>Header Two</h2>'
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
Header Two
----------
<BLANKLINE>

A newline between headers so that a prior underline is not
construed as the next's overline:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<h1>Header One</h1><h2>Header Two</h2>'
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
Header One
==========
<BLANKLINE>
<BLANKLINE>
Header Two
----------
<BLANKLINE>


Lists.

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<ul><li>first</li><li>second</li></ul>'
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
+ first
+ second
<BLANKLINE>
<BLANKLINE>

Ordered lists.

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<ol><li>first</li><li>second</li></ol>'
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
#. first
#. second
<BLANKLINE>
<BLANKLINE>

Nested lists.

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ol><li>1.
... <ul><li>1.1</li><li>1.2</li></ul></li><li>2.</li></ol>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
#. 1.
<BLANKLINE>
    + 1.1
    + 1.2
<BLANKLINE>
#. 2.
<BLANKLINE>
<BLANKLINE>

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ol><li>1.0
... <ul><li>1.1<ul><li>1.1.1</li></ul></li><li>1.2</li></ul></li><li>2.0</li></ol>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
#. 1.0
<BLANKLINE>
    + 1.1
<BLANKLINE>
        + 1.1.1
<BLANKLINE>
    + 1.2
<BLANKLINE>
#. 2.0
<BLANKLINE>
<BLANKLINE>

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<p>some text spanning
... multiple lines, followed by a list
... <ul><li>first</li><li>second</li></ul>and
... more text.</p>'''
>>> parser.feed(preprocess(s))
>>> parser.close()
>>> print writer.getvalue()
<BLANKLINE>
some text spanning multiple lines, followed by a list
<BLANKLINE>
+ first
+ second
<BLANKLINE>
and more text.
<BLANKLINE>
<BLANKLINE>

An additional blankline if the paragraph has been explicitly
closed (should be fixed to give same as previous?):

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<p>some text spanning
... multiple lines, followed by a list</p>
... <ul><li>first</li><li>second</li></ul><p>and
... more text.</p>'''
>>> parser.feed(preprocess(s))
>>> parser.close()
>>> print writer.getvalue()
<BLANKLINE>
some text spanning multiple lines, followed by a list
<BLANKLINE>
<BLANKLINE>
+ first
+ second
<BLANKLINE>
<BLANKLINE>
and more text.
<BLANKLINE>
<BLANKLINE>

Multiline list elements:

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ul><li>first</li><li>oculi omnium in te sperant, Domine, et
... tu das illis escam in tempore opportuno, aperies tu manum tuam et
... impies omne animale in beneplacito.</li><li>third</li></ul>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
+ first
+ oculi omnium in te sperant, Domine, et tu das illis escam in tempore
  opportuno, aperies tu manum tuam et impies omne animale in
  beneplacito.
+ third
<BLANKLINE>
<BLANKLINE>

Multiline nested list elements:

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ul><li>first</li><li>oculi omnium in te sperant, Domine, et
... tu das illis escam in tempore opportuno, aperies tu manum tuam et
... impies omne animale in beneplacito.
... <ol><li>enumerated one</li>
... <li>enumerated two</li></ol>
... </li><li>third</li></ul>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
+ first
+ oculi omnium in te sperant, Domine, et tu das illis escam in tempore
  opportuno, aperies tu manum tuam et impies omne animale in
  beneplacito.
<BLANKLINE>
    #. enumerated one
    #. enumerated two
<BLANKLINE>
+ third
<BLANKLINE>
<BLANKLINE>

List elements with inner html:

>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ul><li>first</li><li><p>oculi omnium in te sperant, Domine, et
... tu das illis escam in tempore opportuno, aperies tu manum tuam et
... impies omne animale in beneplacito.</p></li><li>third</li></ul>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
+ first
+ oculi omnium in te sperant, Domine, et tu das illis escam in tempore
  opportuno, aperies tu manum tuam et impies omne animale in
  beneplacito.
+ third
<BLANKLINE>
<BLANKLINE>

Source code:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<pre>import os
... print os.listdir(os.getcwd())
... 
... def func(x, y, z=None):
...     a = x * y + z
...     return a
...
... </pre>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
.. sourcecode:: python
<BLANKLINE>
    import os
    print os.listdir(os.getcwd())
<BLANKLINE>
    def func(x, y, z=None):
        a = x * y + z
        return a
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>

Source code:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<div><pre>
... import os, sys
... 
... def func(x, y, z=None):
...     a = x * y + z
...     return a
...
... class MyClass(object):
... 
...     attr <span class='op'>=</span> "10"
...
...     attr2 = 5
...     def <span class="s">__init__</span>(self, *args):
...
...         if 1 == 2:
...             def inner(a, b):
...                 return a + b
...             return inner
...         else:
...             return lambda x: x +1
... </pre></div>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
.. sourcecode:: python
<BLANKLINE>
<BLANKLINE>
    import os, sys
<BLANKLINE>
    def func(x, y, z=None):
        a = x * y + z
        return a
<BLANKLINE>
    class MyClass(object):
<BLANKLINE>
        attr = "10"
<BLANKLINE>
        attr2 = 5
        def __init__(self, *args):
<BLANKLINE>
            if 1 == 2:
                def inner(a, b):
                    return a + b
                return inner
            else:
                return lambda x: x +1
<BLANKLINE>
<BLANKLINE>

Source code in a list:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<ul>
... <li>first line which spans multiple lines, I said multiple lines!
... multiple means more than one you freaking numpty, okay? Good!
... Now here's the source code: <pre>import os
... print os.listdir(os.getcwd())
... 
... def func(x, y, z=None):
...     a = x * y + z
...     return a
...
... </pre>
... and here with more multi-line text, within the same list element -
... we want to make sure that the indentation of the next is maintained
... after the literal block.
... </li>
... <li>a second line</li></ul>'''
>>> parser.feed(preprocess(s))
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
+ first line which spans multiple lines, I said multiple lines!
  multiple means more than one you freaking numpty, okay? Good! Now
  here's the source code:
<BLANKLINE>
.. sourcecode:: python
<BLANKLINE>
    import os
    print os.listdir(os.getcwd())
<BLANKLINE>
    def func(x, y, z=None):
        a = x * y + z
        return a
<BLANKLINE>
<BLANKLINE>
  and here with more multi-line text, within the same list element - we
  want to make sure that the indentation of the next is maintained after
  the literal block.
+ a second line
<BLANKLINE>
<BLANKLINE>

Normalise whitespace:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<p>    There   was      an old     man from Nantucket,
... who kept     all         his cash   in a bucket.   His
...     daughter,
...  called Nan,     ran    away\t\t with   a man,   and as for
... the bucket    -   Nan'tucket.</p>'''
>>> parser.feed(preprocess(s))
>>> parser.close()
>>> print writer.getvalue()
<BLANKLINE>
There was an old man from Nantucket, who kept all his cash in a
bucket. His daughter, called Nan, ran away with a man, and as for the
bucket - Nan'tucket.
<BLANKLINE>
<BLANKLINE>


Links

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '<a href="index.html">home</a>'
>>> parser.feed(preprocess(s))
>>> #need to close in order to flush buffer
>>> parser.close()
>>> print writer.getvalue()
`home <index.html>`__
<BLANKLINE>


Losing indentation:

>>> from cStringIO import StringIO
>>> writer=StringIO()
>>> parser = Parser(writer)
>>> s = '''<div class="highlight"><pre><span class="k">import</span> <span class="nn">math</span>
...
... <span class="k">def</span> <span class="nf">is_prime</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
...     <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mf">2</span><span class="p">:</span>
...         <span class="k">return</span> <span class="bp">True</span>
...     <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">xrange</span><span class="p">(</span><span class="mf">2</span><span class="p">,</span> <span class="nb">int</span><span class="p">(</span><span class="n">math</span><span class="o">.</span><span class="n">ceil</span><span class="p">(</span><span class="n">math</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">n</span><span class="p">)))</span> <span class="o">+</span> <span class="mf">1</span><span class="p">):</span>
... 
...         <span class="k">if</span> <span class="n">n</span> <span class="o">%</span> <span class="n">i</span> <span class="o">==</span> <span class="mf">0</span><span class="p">:</span>
...             <span class="k">return</span> <span class="bp">False</span>
... 
...     <span class="k">return</span> <span class="bp">True</span>
... </pre></div>'''
>>> parser.feed(preprocess(s))
>>> #need to close in order to flush buffer
>>> parser.close()
>>> print writer.getvalue()
<BLANKLINE>
<BLANKLINE>
.. sourcecode:: python
<BLANKLINE>
    import math
<BLANKLINE>
    def is_prime(n):
        if n == 2:
            return True
        for i in xrange(2, int(math.ceil(math.sqrt(n))) + 1):
<BLANKLINE>
            if n % i == 0:
                return False
<BLANKLINE>
        return True
<BLANKLINE>
<BLANKLINE>
<BLANKLINE>

"""

from sgmllib import SGMLParser
from StringIO import StringIO
from textwrap import TextWrapper
import sys
import os
import re
import codecs

CODEBLOCK = '.. sourcecode:: python'
BLOCKTAGS = ['div', 'blockquote']
IGNORETAGS = ['title', 'style', 'script']
UNDERLINES = list('=-~`+;')

# Fredrik Lundh, http://effbot.org/zone/re-sub.html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3].lower() == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            import htmlentitydefs
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

class LineBuffer(object):

    def __init__(self):
        self._lines = []
        self._wrapper = TextWrapper()

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, i):
        return self._lines[i]

    def __setitem__(self, i, value):
        self._lines[i] = value

    def clear(self):
        self._lines[:] = []

    def read(self):
        return '\n'.join(self._lines)

    def write(self, s):
        #normalise whitespace
        s = ' '.join(s.split())
        self._lines.extend(self._wrapper.wrap(s))

    def rawwrite(self, s):
        self._lines.extend(s.splitlines())

    def indent(self, numspaces=4, start=0):
        linebuf = self._lines
        n = len(linebuf)
        if n > start:
            indent = ' ' * numspaces
            for i in range(start, n):
                linebuf[i] = indent + linebuf[i]

    def lstrip(self):
        linebuf = self._lines
        for i in range(len(linebuf)):
            linebuf[i] = linebuf[i].lstrip()


class Parser(SGMLParser):

    def __init__(self, writer=sys.stdout):
        SGMLParser.__init__(self)
        self.writer = writer
        self.stringbuffer = StringIO()
        self.linebuffer = LineBuffer()
        self.verbatim = False
        self.lists = []
        self.ignoredata = False
        self.inblock = 0
        self.nobreak = False
        self.link = None

    def close(self):
        self.writeline()
        SGMLParser.close(self)

    def flush(self):
        if self.linebuffer:
            if self.inblock > 1:
                indent = 4 * (self.inblock - 1)
                self.linebuffer.indent(indent)
            self.writer.write(unescape(self.linebuffer.read()))
            self.linebuffer.clear()

    def flush_stringbuffer(self):
        sbuf = self.stringbuffer.getvalue()
        if not sbuf:
            return
        elif self.linebuffer:
            self.linebuffer[-1] += sbuf
        else:
            self.linebuffer.write(sbuf)
        self.clear_stringbuffer()

    def clear_stringbuffer(self):
        #self.stringbuffer.reset()
        self.stringbuffer.seek(0)
        self.stringbuffer.truncate()

    def data(self, text):
        self.stringbuffer.write(text)

    def pending(self):
        return self.stringbuffer.tell() or self.linebuffer

    def write(self, text=''):
        self.flush_stringbuffer()
        self.flush()
        self.writer.write(unescape(text))

    def writeline(self, text=''):
        self.write(text + '\n')

    def writestartblock(self, text=''):
        if self.pending():
            self.writeline()
        self.writeline()
        self.writeline(text)

    def writeendblock(self, text=''):
        self.writeline(text)
        self.writeline()

    def writeblock(self, text=''):
        self.writestartblock(text)
        self.writeline()

    def handle_data(self, data):
        if self.ignoredata:
            return
        elif self.verbatim:
            self.data(data)
        else:
            self.data(' '.join(data.splitlines()))

    def unknown_starttag(self, tag, attrs):
        if tag in IGNORETAGS:
            self.ignoredata = True
        elif len(tag) == 2 and tag[0] == 'h':
            self.writestartblock()
        elif tag == 'br':
            if self.verbatim:
                self.data('\n')
            elif not self.inblock:
                self.writeline()
            else:
                self.data(' ')
        elif not self.verbatim:
            self.data(' ')

    def unknown_endtag(self, tag):
        self.ignoredata = False
        if len(tag) == 2 and tag[0] == 'h':
            self.flush_stringbuffer()
            if self.linebuffer:
                linebuf = self.linebuffer
                linebuf[-1] = linebuf[-1].strip()
                char = UNDERLINES[int(tag[1])-1]
                linebuf.write(char * len(linebuf[-1]))
                self.writeline()
        #elif tag in BLOCKTAGS and self.pending():
        #    if self.lists:
        #        self.end_li()
        #    else:
        #        self.writeline()
        elif not self.verbatim:
            self.data(' ')

    def start_a(self, attrs):
        href = dict(attrs).get('href', None)
        if not href or href.startswith('#'):
            return
        self.data('`')
        self.link = href

    def end_a(self):
        if self.link:
            self.data(' <%s>`__' % self.link)
            self.link = None

    def start_pre(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        #self.inblock += 1
        self.verbatim = True
        self.writeblock(CODEBLOCK)

    def end_pre(self):
        sbuf = self.stringbuffer.getvalue()
        if sbuf:
            self.linebuffer.rawwrite(sbuf)
            self.linebuffer.indent(4)
        self.clear_stringbuffer()
        self.writeendblock()
        #self.inblock -= 1
        self.verbatim = False

    def start_ul(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        else:
            self.writeline()
        self.lists.append('+ ')
        self.inblock += 1

    def end_ul(self):
        self.end_li()
        self.lists.pop()
        self.inblock -= 1
        if self.inblock:
            self.writeline()
        else:
            self.writeendblock()

    def start_ol(self, attrs):
        if self.lists:
            self.end_li()
            self.writeline()
        else:
            self.writeline()
        self.lists.append('#. ')
        self.inblock += 1

    def end_ol(self):
        self.end_li()
        self.lists.pop()
        self.inblock -= 1
        if self.inblock:
            self.writeline()
        else:
            self.writeendblock()

    def start_p(self, attrs):
        if self.verbatim:
            self.writeline()
        elif not self.inblock:
            self.writeline()

    def end_p(self):
        if self.inblock:
        #self.flush_stringbuffer()
            if self.verbatim:
                self.writeline()
            else:
                return
        else:
            self.linebuffer.lstrip()
            self.writeline()

    def start_li(self, attrs):
        self.writeline()
        self.data(self.lists[-1])
    
    def end_li(self):
        self.flush_stringbuffer()
        linebuf = self.linebuffer
        if linebuf and linebuf[0] and linebuf[0].lstrip()[:2] in ['+ ', '#.']:
            start=1
        else:
            # the start of the <li> has already been written, perhaps because
            # there was a <pre> block
            start = 0
        self.linebuffer.indent(len(self.lists[-1]), start=start)
        self.write()

    def start_dl(self, attrs):
        self.writeline()
        self.inblock += 1
        self.nobreak = True

    def end_dl(self):
        self.nobreak = False
        self.writeline()
        self.inblock -= 1

    def start_dt(self, attrs):
        self.data(':')

    def end_dt(self):
        self.data(':')

    def start_dd(self, attrs):
        self.data(' ')

    def end_dd(self):
        self.flush_stringbuffer()
        self.linebuffer.indent(2, start=1)
        self.writeline()

    def start_em(self, attrs):
        self.data(' *')

    def end_em(self):
        self.data('*')

    def start_b(self, attrs):
        self.data(' **')

    def end_b(self):
        self.data('**')

    def start_code(self, attrs):
        self.data(' `')

    def end_code(self):
        self.data('`')

    def start_span(self, attrs):
        pass

    def end_span(self):
        pass

    def start_body(self, attrs):
        pass

    def end_body(self):
        self.end_p()
try:
    from BeautifulSoup import BeautifulSoup, NavigableString

    class ShlurpUpYourShloup(BeautifulSoup):
        '''preserve whitespace in <pre>'''
        def endData(self, containerClass=NavigableString):
            if self.currentData:
                currentData = ''.join(self.currentData)
                if not currentData.strip():
                    if '\n' in currentData:
                        currentData = '\n'
                    else:
                        # just changed the following line
                        # original: currentData = ' '
                        currentData = u' ' * len(currentData)
                self.currentData = []
                if self.parseOnlyThese and len(self.tagStack) <= 1 and \
                    (not self.parseOnlyThese.text or \
                        not self.parseOnlyThese.search(currentData)):
                    return
                o = containerClass(currentData)
                o.setup(self.currentTag, self.previous)
                if self.previous:
                    self.previous.next = o
                self.previous = o
                self.currentTag.contents.append(o)

except ImportError:
    def ShlurpUpYourShloup(text, *args, **kw):
        return text

def readsoup(infile, convert='html', encoding='utf8'):
    if hasattr(infile, 'read'):
        text = infile.read()
    else:
        text = open(infile, 'rb').read()
    #for br in ['<br>', '<br/>', '<br />']:
    #    text = text.replace(br, '\n')
    #    text = text.replace(br.upper(), '\n')
    return str(BeautifulSoup(text, convertEntities=convert,
                                            fromEncoding=encoding))

def html2rest(html, writer=sys.stdout):
    parser = Parser(writer)
    parser.feed(html)
    parser.close()

if __name__ == "__main__":
    data = None
    if sys.argv[1:]:
        arg = sys.argv[1]
        if arg == '--test':
            import doctest
            #options = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
            doctest.testmod()#optionflags=options)
        elif arg.startswith('http://'):
            import urllib
            data = urllib.urlopen(arg)#.read()
        else:
            data = codecs.open(arg, 'rb', 'utf8')#.read()
    else:
        data = sys.stdin#.read()
    if data is not None:
        html2rest(readsoup(data))
        #sys.stdout.write(rest.encode('ascii', 'replace'))


