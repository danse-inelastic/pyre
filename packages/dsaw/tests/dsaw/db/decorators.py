
class Column(object):


    def type(self):
        raise NotImplementedError("class %r must override 'type'" % self.__class__.__name__)


    def getFormattedValue(self, instance, cls = None):
        'obtain value that is formatted for db access'
        value = self.__get__(instance, cls = cls)
        return self._format( value )
    

    def declaration(self):
        text = [ self.type() ]
        if self.default is not None:
            text.append("DEFAULT %r" % self.default)
        if self.constraints:
            text.append(self.constraints)

        return " ".join(text)


    def __init__(self, name, default=None, auto=False, constraints=None, meta=None):
        self.name = name
        self.default = default
        self.auto = auto
        self.constraints = constraints

        if meta is None:
            meta = {}
        self.meta = meta

        return


    def __get__(self, instance, cls=None):

        # attempt to get hold of the instance's attribute record
        try:
            return instance._getColumnValue(self.name)

        # instance is None when accessed as a class variable
        except AttributeError:
            # catch bad descriptors or changes in the python conventions
            if instance is not None:
                import journal
                firewall = journal.firewall("pyre.inventory")
                firewall.log("AttributeError on non-None instance. Bad descriptor?")

            # interpret this usage as a request for the trait object itself
            return self

        except KeyError:
            # look up the registered default value
            default = self.default

            # if we don't have a default, mark this column as uninitialized
            if default is None:
                return default

            # otherwise, store the default as the actual field value
            return instance._setColumnValue(self.name, default)


        # not reachable
        import journal
        journal.firewall('pyre.db').log("UNREACHABLE")
        return None


    def __set__(self, instance, value):
        value = self._cast(value)
        return instance._setColumnValue(self.name, value)


    def _cast(self, value):
        return value


    def _format(self, value):
        'format the given value so that it can be used in db cmd'
        #by default, just return the value
        return value


class varChar(Column):


    def type(self):
        return "character varying (%d)" % self.length


    def __init__(self, name, length, default="", f, **kwds):
        Column.__init__(self, name, default, **kwds)
        self.length = length
        return

#def varchar(**kwds):
#    from VarChar import VarChar
#    return VarChar(**kwds)

# the goal is to wrap cake with the varChar class attribute--just like def varchar would do...

#@varChar
myAttribute = 'cake'

class myDecorator(object):

    def __init__(self, f):
        print "inside myDecorator.__init__()"
        f() # Prove that function definition has completed

    def __call__(self):
        print "inside myDecorator.__call__()"

@myDecorator
def aFunction():
    print "inside aFunction()"

print "Finished decorating aFunction()"

aFunction()
