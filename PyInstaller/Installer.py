# appmgr_default.py
import appuifw, appstdio
appstdio.name()
try: import series60_console, sys, e32, os
except (MemoryError, SymbianError): appstdio.memerr()

class installer:
  PYTHON_PATH='\\system\\apps\\python'; APPMGR_PATH='\\system\\apps\\PyInstaller\\AppCreationInfo'; SCRIPT_PATH='\\Documents\\scripts\\'; LIB_PATH='\\system\\libs'; APPS_PATH='\\system\\apps'; PYTHON_EXTS=['.py', '.pyc', '.pyo', '.pyd']; PYTHON_LIB_EXTS=['.pyc', '.pyo', '.pyd']
  def __init__(self):
   appuifw.app.title, appuifw.app.screen = u'Python Installer', 'normal'
   if (type(sys.stderr), type(sys.stdout)) == (file, file):
    my_console = series60_console.Console()
    appuifw.app.body = my_console.text
    sys.stderr = sys.stdout = my_console
   print "Python for S60\nInstaller\nVersion "+e32.pys60_version+'\n'
   appuifw.app.menu = [
    (u"Install",self.install),
    (u"About",self.about_pyinstaller),
    (u"Exit", appuifw.app.set_exit)]
   global launched_as_file
   try: launched_as_file
   except NameError: self.run_args = sys.argv
   else: self.run_args = [sys.argv[0],launched_as_file]
   try: print 'Installing:\n%s\n'%self.run_args[1]
   except IndexError: pass
   e32.ao_sleep(0)
   try: launched_as_file
   except NameError: pass
   this_dir = os.path.split(appuifw.app.full_name())[0]
   self.noted=0

  def note_once(self,msg_ind,type_ind):
   if not self.noted:
    e32.ao_sleep(0)
    msgs=['Installation complete', 'Installation canceled', 'Installation failed', 'Nothing to install']
    types1=['error','info','conf']
    types2=['! ','i ','/ ']
    if type(msg_ind)==int: msg=msgs[msg_ind]
    else: msg = msg_ind
    type2=types2[type_ind]
    type1=types1[type_ind]
    try: launched_as_file
    except NameError:
     try: print '%s: %s: %s'%(self.menu1[self.index].title(),type2,msg)
     except (NameError, AttributeError, TypeError): print '%s: %s'%(type2,msg)
     except IndexError: print 'menu[%s]: %s: %s'%(self.index,type2,msg)
    appuifw.note(unicode(msg),type1)
    self.noted=1

  def about_pyinstaller(self): appuifw.note(u"Python script, lib module, and app installer")

  def python_drive(self):
      for drive in [str(x) for x in e32.drive_list()]:
          if os.path.isfile(os.path.join(drive, self.PYTHON_PATH, 'python.app')):
              return drive
      raise AssertionError, "Python not found"

  def do_copy(self, src, dst):
      if not os.path.isdir(dst):
          os.mkdir(os.path.split(dst))
      try: e32.file_copy(unicode(dst), unicode(src))
      except SymbianError: self.note_once('File already in use',0)

  def script_install(self, filename):
      temp=appuifw.query(u'File name:','text',unicode(os.path.split(filename)[1]))
      if not temp: self.note_once(1, 1); return
      dst = os.path.join(dst_dir, temp)
      if os.path.exists(os.path.join(self.python_drive(), self.SCRIPT_PATH, os.path.split(filename)[1])):
       if appuifw.query((u'Replace existing?\n%s'%os.path.split(filename)[1]),'query'):
        self.do_copy(filename, os.path.join(self.python_drive(), self.SCRIPT_PATH))
       else: self.note_once(1,1)
      else:
        self.do_copy(filename, os.path.join(self.python_drive(), self.SCRIPT_PATH))

  def lib_install(self, filename):
      file_root = os.path.splitext(os.path.split(filename)[1])[0]
      matching_lib_names = [file_root+x for x in self.PYTHON_EXTS]
      for p in sys.path[1:]:
          for n in matching_lib_names:
              matching_name = os.path.join(p, n)
              if os.path.exists(matching_name):
                  if appuifw.query(u'Replace existing?\n'+unicode(n),'query'):
                      os.remove(matching_name)
                  else: return
      self.do_copy(filename, os.path.join(self.python_drive(), self.LIB_PATH))

  def standalone_install(self, filename):
      def reverse(L): L.reverse(); return L
      def atoi(s):
          # Little-endian conversion from a 4-char string to an int.
          sum = 0L
          for x in reverse([x for x in s[0:4]]): sum = (sum << 8) + ord(x)
          return sum
      def itoa(x):
          # Little-endian conversion from an int to a 4-character string.
          L=[chr(x>>24), chr((x>>16)&0xff), chr((x>>8)&0xff), chr(x&0xff)]
          L.reverse()
          return ''.join(L)
      try:
          offset = int(file(os.path.join(self.python_drive(), self.APPMGR_PATH,
                                         'uid_offset_in_app')).read(), 16)
      except: offset = None
      temp=appuifw.query(u'Application name:','text',unicode(os.path.splitext(os.path.split(filename)[1])[0]))
      if temp: app_rootname = str(temp)
      else: self.note_once(1, 1); return
      app_dir = os.path.join(self.python_drive(), self.APPS_PATH, app_rootname)

      uid_status=1; uid_text='0x1'
      while uid_status==1:
       script = open(filename).read()
       uidpos = script.find('SYMBIANUID')+10
       try: uidpos += script[uidpos:uidpos+5].index('0x')+2
       except ValueError: pass
       else: uid_text = '0x'+script[uidpos:uidpos+8]
       uid_input = appuifw.query(u'UID (8 digits hexadecimal)\n 0x12345678', 'text', unicode(uid_text))
       if uid_input:
        try: uid = int(uid_input, 16)
        except:
         appuifw.note(u'Bad UID value', 'error')
         uid_text=uid_input
        else:
         try: crc1 = itoa(e32._uidcrc_app(uid))
         except ValueError: appuifw.note(u'Bad UID value', 'error')
         else: uid_status = 2
       else: uid_status = 0
      if not uid_status: self.note_once(1, 1); return

      # copy the script to application's directory as default.py
      if not os.path.isdir(app_dir):
          os.mkdir(app_dir)
      try: e32.file_copy(unicode(os.path.join(app_dir, 'Default.py')),
                    unicode(filename))
      except SymbianError: self.note_once('File already in use', 0)
      # copy the template .app file to application directory with proper name
      # and set the UID and checksum fields suitably
      template_dotapp = file(os.path.join(self.python_drive(), self.APPMGR_PATH, 'pyapp_template.tmp'))
      dotapp_name = app_rootname + '.app'
      dotapp = file(os.path.join(app_dir, dotapp_name), 'w')
      appbuf = template_dotapp.read()
      csum = atoi(appbuf[24:28])
      crc2 = itoa(( uid + csum ) & 0xffffffffL)
      if offset:
          temp = appbuf[0:8] + itoa(uid) + crc1 + appbuf[16:24] + crc2 +\
                 appbuf[28:offset] + itoa(uid) + appbuf[(offset+4):]
      else: temp = appbuf[0:8] + itoa(uid) + crc1 + appbuf[16:24] + crc2 + appbuf[28:]
      dotapp.write(temp)
      # copy the template .rsc file to application directory with proper name
      rsc_name = app_rootname + '.rsc'
      e32.file_copy(unicode(os.path.join(app_dir, app_rootname + '.rsc')),
                    unicode(os.path.join(self.python_drive(), self.APPMGR_PATH, 'pyrsc_template.tmp')))

  def execfile1(self, filename):
      saved_io=appuifw.app.title,appuifw.app.screen,appuifw.app.body,sys.stderr,sys.stdout
      e32.ao_sleep(0)
      execfile(filename,globals())
      appuifw.app.title,appuifw.app.screen,appuifw.app.body,sys.stderr,sys.stdout=saved_io
      self.note_once('Script exited',1)

  def exit_wait(self): appuifw.note(u"Please wait", "info")

  def run(self, params):
   filename = params[1]
   appuifw.app.title = unicode(os.path.split(filename)[1])
   ext = os.path.splitext(filename)[1].lower()
   if ext in self.PYTHON_EXTS:
    source_path = os.path.splitdrive(filename)[1].lower()
    # It's safe to exit if we have been started from the Messaging
    # app, but not if we have been started from e.g. the web
    # browser, since then the whole browser would exit. The
    # default is to not exit the app, since that's safer.
    should_exit=source_path.startswith('\\system\\mail')
    if ext in self.PYTHON_LIB_EXTS:
     actions = [lambda: self.lib_install(filename)]
     self.menu = [u"Lib module"]
     self.menu1 = [u"Lib"]
    elif ext in self.PYTHON_EXTS:
     actions = [lambda: self.execfile1(filename),
                   lambda: self.standalone_install(filename),
                   lambda: self.script_install(filename),
                   lambda: self.lib_install(filename)]
     self.menu = [u"Run now",
                 u"Application",
                 u"Script",
                 u"Lib module"]
     self.menu1 = [u"Run", u"App", u"Script", u"Lib"]

    self.index = appuifw.popup_menu(self.menu, u"Install as")
    try:
     if not self.index == None:
      appuifw.app.exit_key_handler = self.exit_wait
      e32.ao_yield()
      actions[self.index]()
      self.note_once(0,2)
     else: self.noted=1
    finally:
      appuifw.app.exit_key_handler = None
      if should_exit: appuifw.app.set_exit()

  def install(self):
   self.noted=0
   try: self.run(self.run_args)
   except IndexError: self.note_once(3,1)
   else: self.note_once(2,0)

installer().install()
