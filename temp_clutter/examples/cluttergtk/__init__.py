import sys

# fixes weird linker bugs on nvidia
try:
    import dl
    sys.setdlopenflags(dl.RTLD_LAZY|dl.RTLD_GLOBAL)
except ImportError:
    try:
        import platform
        if platform.system() == 'Linux' and platform.machine() in \
                ['x86_64', 'amd64']:
            try:
                import ctypes, ctypes.util
                ctypes.CDLL(ctypes.util.find_library('GL'),
                        mode=ctypes.RTLD_GLOBAL)
            except:
                pass
    except ImportError:
        pass

# For broken embedded programs which forgot to call Sys_SetArgv
if not hasattr(sys, 'argv'):
    sys.argv = []

# load the required modules:
import gobject as _gobject

ver = getattr(_gobject, 'pygobject_version', ())
if ver < (2, 11, 1):
    raise ImportError("PyClutter requires PyGObject 2.11.1 or higher, but %s was found" % (ver,))

if 'cluttergtk._cluttergtk' in sys.modules:
    _cluttergtk = sys.modules['cluttergtk._cluttergtk']
else:
    from cluttergtk import _cluttergtk

from cluttergtk._cluttergtk import *
__version__ = _cluttergtk.__version__
