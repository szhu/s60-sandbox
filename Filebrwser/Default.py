import appstdio
appstdio.name()
appstdio.stderr()
appstdio.stdout()
try: execfile(r'E:\System\Apps\Filebrwser\Filebrowser.py', globals())
except (MemoryError, SymbianError): appstdio.memerr()
