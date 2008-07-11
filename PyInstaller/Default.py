import appstdio
try: execfile(r'E:\System\Apps\PyInstaller\Installer.py')
except (MemoryError, SymbianError): appstdio.memerr()
except:
 appstdio.stderr()
 import traceback; traceback.print_exc()
