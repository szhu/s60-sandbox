import appstdio
appstdio.name()
appstdio.stderr()
try:
 execfile(r'E:\System\Apps\TextEdit\TextEdit.py',globals())
 text()
except (MemoryError, SymbianError): appstdio.memerr()
except:
 appstdio.stderr()
 import traceback; traceback.print_exc()
 import appuifw; appuifw.app.set_exit()
