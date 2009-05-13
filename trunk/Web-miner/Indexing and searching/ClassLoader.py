import sys

class ClassLoader(object):

    @classmethod
    def loadClass(cls, name, module=None):

        if module is None:
            lastDot = name.rindex('.')
            module = name[:lastDot]
            name = name[lastDot+1:]

        try:
            m = __import__(module, globals(), locals(), name)
        except ImportError:
            raise
        except SyntaxError:
            raise
        except:
            x, value, traceback = sys.exc_info()
            raise ImportError, value, traceback

        try:
            return getattr(m, name)
        except AttributeError:
            raise ImportError, "Module %s has no class %s" %(module, name)

#    loadClass = classmethod(loadClass)