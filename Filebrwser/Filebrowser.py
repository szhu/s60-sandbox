import appuifw
appuifw.app.title = u"File Browser"
try:
 import sys, os, e32, dir_iter, appstdio
 from key_codes import EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow, EKey1, EKey2, EKey3, EKey4, EKey5, EKey6, EKey7, EKey8, EKey9, EKey0, EKeyStar, EKeyHash, EKeyBackspace
except (MemoryError, SymbianError): appstdio.memerr(); appuifw.app.set_exit()

class Filebrowser:
    def __init__(self):
        self.script_lock = e32.Ao_lock()
        self.dir_stack = []
        self.current_dir = dir_iter.Directory_iter()
        sys.stdout=lambda: None; sys.stdout.write = lambda x: [appuifw.note(u'%s'%x) for i in range(not x or x.replace('\n','')!='')]
    def run(self):
        self.listmode='full'; self.screenmode=1
        try: execfile('E:\System\Apps\Filebrwser\Filebrowser.ini')
        except: appuifw.note(u'Settings file damaged','error')
        self.toggle_listmode(0)
        #self.script_lock.wait()

    def delete(self):
      if self.current_dir.len==0 or self.current_dir.at_root: return
      global focused_item; focused_item = index = self.lb.current()
      try:
       if os.path.isdir(self.current_dir.entry(index)): kind='folder'
       else: kind='file'
      except IndexError: kind='folder'
      if appuifw.query(u'Delete '+kind+'?', 'query'):
        try:
          if kind=='file': os.remove(self.current_dir.entry(index))
          if kind=='folder': os.rmdir(self.current_dir.entry(index))
          focused_item = index
        except:
          errtype, value = map(str, (sys.exc_type, sys.exc_value))
          if errtype=='exceptions.OSError' and value[:10]=='[Errno 13]': errtype, value='', 'Permission denied'
          if errtype=='exceptions.OSError' and value[:10]=='[Errno 17]': errtype, value='', 'Folder not empty'
          if errtype: errtype+=':\n'
          appuifw.note(unicode(errtype+value), "error")
        self.refresh(dir_changed=0)

    def toggle_listmode(self, toggle=1, init_lb=1):
     modes=['compact', 'full'] 
     if toggle:
      global focused_item; focused_item=self.lb.current()
      self.listmode=modes[not modes.index(self.listmode)]
     open('E:\System\Apps\Filebrwser\Filebrowser.ini', 'w').write("self.listmode = " + repr(self.listmode) + "\nself.screenmode = " + repr(self.screenmode)+"\n")
     if self.listmode==modes[1]:
      if init_lb: appuifw.app.body = self.lb = appuifw.Listbox([(u'', u'Loading...')],self.lbox_observe)
      if self.screenmode: self.listmode_num=4
      else: self.listmode_num=3
     elif self.listmode==modes[0]:
      if init_lb: appuifw.app.body = self.lb = appuifw.Listbox([(u'Loading...')], self.lbox_observe)
      if self.screenmode: self.listmode_num=9
      else: self.listmode_num=6
     e32.ao_sleep(0)
     self.refresh(refresh_files=0)
    def toggle_screenmode(self):
     self.screenmode=not self.screenmode
     e32.ao_sleep(0)
     global focused_item; focused_item=self.lb.current()
     self.toggle_listmode(0, 0)

    def loading(self):
        if self.listmode=='compact': self.lb.set_list([(u'Loading...')], 0)
        elif self.listmode=='full': self.lb.set_list([(u'',u'Loading...')], 0)
        e32.ao_sleep(0)
    def refresh(self, refresh_files=1, refresh_ui=1, dir_changed=1, set_list=1):
        global focused_item
        if not dir_changed: focused_item=self.lb.current()
        try: focused_item
        except NameError: focused_item=0
        if not refresh_files:
          try: self.last_dir
          except AttributeError: refresh_files=2
        if refresh_files: self.loading(); self.entries = self.last_dir = self.current_dir.list_repr()
        if refresh_ui:
          appuifw.app.body=self.lb
          if self.screenmode:
           if self.listmode=='compact': appuifw.app.screen='full'
           if self.listmode=='full': appuifw.app.screen='large'
          else: appuifw.app.screen='normal'
          menu=[[unicode(x), []] for x in ('File', 'Go', 'Edit', 'View', 'Settings')]
          if self.current_dir.len: menu[1][1]+=[(u'Go to item...',self.surface_find)]
          menu[1][1]+=[(u'Refresh',lambda: self.refresh(dir_changed=0))]
          if self.current_dir.len:
           menu[0][1]+=[(u'Open / Select action',self.lbox_observe)]
           if not self.current_dir.at_root: menu[0][1]+=[(u'Delete',self.delete)]
          menu[3][1]+=[
            (u'Screen mode: '+appuifw.app.screen, self.toggle_screenmode),
            (u'List mode: '+self.listmode, self.toggle_listmode)]
          menu+=[
           (u'About', lambda: appuifw.note(u'Python')),
           (u'Exit', appuifw.app.set_exit)]
          for i in range(len(menu)):
           while len(menu)>i:
            if menu[i][1]==[]: del menu[i]
            elif type(menu[i][1])==list:
             menu[i][1]=tuple(menu[i][1]); menu[i]=tuple(menu[i])
             if len(menu[i][1])==1: menu[i]=menu[i][1][0]
             break
            else: break
          appuifw.app.menu=menu
          self.lb.bind(EKeyRightArrow, lambda: self.lbox_observe(pass_files=1)); self.lb.bind(EKeyLeftArrow, lambda: self.lbox_observe(-1))
          self.lb.bind(EKeyBackspace, self.delete)
          self.lb.bind(EKeyUpArrow, lambda: self.chg_pos(wrap='up'))
          self.lb.bind(EKeyDownArrow, lambda: self.chg_pos(wrap='down'))
          self.lb.bind(EKey3, lambda: self.chg_pos(-self.listmode_num)); self.lb.bind(EKey9, lambda: self.chg_pos(self.listmode_num))
          self.lb.bind(EKey5, lambda: self.chg_pos(-1, 1)); self.lb.bind(EKey6, lambda: self.chg_pos(0, len(self.entries)))
        if self.current_dir.len==0:
          if self.listmode=='compact': self.last_dir=[(u"Empty Folder",)]
          elif self.listmode=='full': self.last_dir=[(u"", u"Empty Folder")]

        if self.current_dir.at_root: appuifw.app.title=u'File Browser'
        else:
         current_dir=self.current_dir.name()
         if current_dir[-1]=='\\': current_dir=current_dir[:-1]
         appuifw.app.title=appstdio.nice_unicode(current_dir.split('\\')[-1])
        if self.listmode=='compact': self.entries = map(lambda x: x[0], self.last_dir)
        elif self.listmode=='full': self.entries = self.last_dir
        if set_list: self.lb.set_list(self.entries, focused_item)

    #def self.current_dir.name()
    def surface_find(self):
     global focused_item
     appuifw.app.screen='normal'
     focused_item=appuifw.selection_list(map(lambda x: x[0], self.last_dir), 1)
     self.refresh(refresh_files=0,dir_changed=focused_item>=0)
    def chg_pos(self, value=0, base=None, wrap=0):
        if type(base)==int: focused_item=base+value
        else: focused_item=self.lb.current()+value
        if wrap=='up' and focused_item==0: focused_item=len(self.entries)
        elif wrap=='down' and focused_item==len(self.entries)-1: focused_item=0
        else:
          wrap=0
          if focused_item>len(self.entries): focused_item=len(self.entries)
          elif focused_item<0: focused_item=0
        if self.listmode in ('compact','full') and (value or base or wrap in ('up','down')):
          self.lb.set_list(self.entries, focused_item)

    def exit_applet(self): self.applet_running=0
    def lbox_observe(self, ind = None, pass_files=0, allow_exe=0):
        global focused_item; focused_item = 0
        if not ind == None: index = ind
        else: index = self.lb.current()
        
        if self.current_dir.at_root:
          if ind == -1: return
          self.dir_stack.append(index)
          self.current_dir.add(index)
        elif index == -1:
          focused_item = self.dir_stack.pop()
          self.current_dir.pop()
        elif not self.current_dir.len: return
        elif os.path.isdir(self.current_dir.entry(index)):
          self.dir_stack.append(index)
          self.current_dir.add(index)
        else:
          focused_item = self.lb.current()
          if pass_files: return
          item = self.current_dir.entry(index)
          if os.path.splitext(item)[1].lower() == '.py':
            i = appuifw.popup_menu([u"Run",u"Install",u"Open"])
            if i==None: return
            elif i==2 and appuifw.query(u'Warning:\nOperation may close file browser.\nContinue?','query'): appuifw.Content_handler().open_standalone(item); return
            import sys
            saved_io = appuifw.app.screen, sys.stderr, sys.stdout, appuifw.app.exit_key_handler, appuifw.app.body
            appuifw.app.screen='normal'; appuifw.app.exit_key_handler=self.exit_applet; e32.ao_sleep(0)
            if i==0:
              try: execfile(item, globals())
              except: import traceback; traceback.print_exc()
            elif i==1:
              global launched_as_file; launched_as_file=item
              try: execfile('E:\System\Apps\PyInstaller\Default.py', globals(), locals())
              except MemoryError: appuifw.note(appuifw.app.name+u':\nMemory full.\nClose some applications and try again.','error',1)
              except: import traceback; traceback.print_exc()
              self.applet_running=1
              while self.applet_running: appuifw.app.exit_key_handler=self.exit_applet; e32.ao_sleep(0)
              if 'my_console' in dir(): del my_console
            elif i==0: appuifw.note(u'Script exited')
            appuifw.app.screen, sys.stderr, sys.stdout, appuifw.app.exit_key_handler, appuifw.app.body = saved_io
            self.refresh(refresh_files=0, dir_changed=0, set_list=0)

          else:
              try:
               if allow_exe:
                #import e32
                if item[-4:].lower()=='.exe': e32.start_exe(item,'')
                elif item[-4:].lower()=='.app': e32.start_exe(r'Z:\system\programs\AppRun.exe', item)
                else: appuifw.Content_handler().open_standalone(item)
               else: appuifw.Content_handler().open_standalone(item)
              except:
                import sys
                errtype, value = map(str, (sys.exc_type, sys.exc_value))
                if errtype=='exceptions.TypeError' and value=='mime type not supported': errtype, value='', 'Unknown file format'
                if errtype=='exceptions.TypeError' and value=='executables not allowed':
                 if allow_exe: errtype, value='', "Can't open executables"
                 else: errtype, value='', ''; self.lbox_observe(allow_exe=1)
                if errtype=='exceptions.OSError' and value[:10]=='[Errno 13]': errtype, value='', 'Permission denied'
                if errtype=='exceptions.SymbianError' and value[:10]=='[Errno -4]': errtype, value='', "Memory full"
                if errtype: errtype+=':\n'
                if errtype or value: appuifw.note(unicode(errtype+value), "error")
          return
        self.refresh()

if __name__=='__main__': Filebrowser().run()
