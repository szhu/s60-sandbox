# dir_iter.py
# Utility module for filebrowser.

import sys, os, time, e32, appstdio

class Directory_iter:
    def __init__(self, drive_list=None):
        self.drives=lambda: [((i, u"Drive")) for i in e32.drive_list()]
        self.at_root = 1
        self.len = len(self.drives())
        self.path = '\\'

    def pop(self):
        if os.path.splitdrive(self.path)[1] == '\\':
            self.path = '\\'
            self.at_root = 1
        else:
            self.path = os.path.split(self.path)[0]

    def add(self, i):
        if self.at_root:
            self.path = str(self.drives()[i][0]+u'\\')
            self.at_root = 0
        else:
            self.path = os.path.join(self.path, os.listdir(self.name())[i])

    def name(self):
        return self.path

    def list_repr(self):
        if self.at_root:
            self.len = len(self.drives())
            return self.drives()
        else:
            def item_format(i):
                full_name = os.path.join(str(self.name()), i)
                try: time_field = time.strftime("%m/%d/%Y %H:%M",\
                               time.localtime(os.stat(full_name).st_mtime))
                except: time_field = "--/--/---- --:--"
                if os.path.isdir(full_name):
                    name_field = i+"\\"
                    size, size_unit= 'Folder',''
                else:
                  name_field = i
                  try: size = os.stat(full_name).st_size; size_unit='b'
                  except: size = '?'; size_unit='b'
                  else:
                    if size>=1200000000: size = round(float(os.stat(full_name).st_size)/1000000000, 1); size_unit='GB'
                    elif size>=1200000: size = round(float(os.stat(full_name).st_size)/1000000, 1); size_unit='MB'
                    elif size>=1200: size = round(float(os.stat(full_name).st_size)/1000, 1); size_unit='kb'
                info_field = time_field+"   "+str(size)+' '+size_unit
                try: name_field=unicode(name_field)
                except UnicodeError: name_field=appstdio.nice_unicode(name_field)
                except: import traceback; traceback.print_exc()#name_field=u" ??? "
                return name_field, unicode(info_field)
            try: I=map(item_format, os.listdir(self.name())); self.len = len(I); return I
            except:
             import traceback
             traceback.print_exc()
             return (Exception,)+sys.exc_info()

    def entry(self, i, list1=None):
        if list1==None: list1=os.listdir(self.name())
        return os.path.join(self.name(), list1[i])
