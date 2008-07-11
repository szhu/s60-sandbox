import sys, os, appuifw, e32, appstdio
class text:
 from key_codes import EKeyYes, EKeyNo, EKeyMenu, EKeySelect
 def __init__(self):
  appuifw.app.body=self.body=appuifw.Text()
  self.body.color=0; self.body.font=u'LatinPlain12'
  appstdio.stdout()
  #print sys.argv
  self.is_open=0; self.search_str=''; self.replace_str=''
  self.cache=None; self.wait=0; self.save_confirm=0
  self.inputs_split=u'\u2029'+u'-'*20+u'\u2029'
  self.defaults={'title':u'TextEdit', 'text':u'\u2029'}
  self.path=r'E:\Documents\Text'+'\\'; self.recent=[]; self.recents_len=30
  self.body.set(self.defaults['text'])
  appuifw.app.exit_key_handler=self.close_or_exit
  self.body.bind(self.EKeyYes, lambda: self.save(0))
  self.body.bind(self.EKeyMenu, self.memory_lock)
  self.body.bind(self.EKeyNo, self.memory_lock)
  self.body.bind(self.EKeySelect, self.position)
  try: execfile(r'C:\System\Apps\TextEdit\TextEdit.ini')
  except: pass
  self.refresh()

 def refresh(self):
  self.wait=0
  self.body.color=0; self.body.font=u'LatinPlain12'
  if self.is_open: appuifw.app.title=unicode(os.path.split(self.path)[1])
  else: appuifw.app.title=self.defaults['title']
  menu=[[unicode(x), []] for x in ('File','Edit')]
  menu[0][1]+=[(u'Open path...', self.open_as)]
  if self.is_open: menu[0][1]+=[(u'Save', self.save)]
  menu[0][1]+=[(u'Save as...', lambda: self.save(save_as=1))]
  menu[1][1]+=[(u'Find...', self.find),
         (u'Find & Replace...', lambda: self.find(replace=1)),
         (u'Position...', self.position)]
  if self.is_open: menu[0][1]+=[(u'Revert', self.revert),
          (u'Close', self.close)]
  if len(self.recent): menu.insert(0, (u'Open recent', tuple(map(lambda x: (unicode(os.path.split(x)[1]), lambda: self.open_path(x)), self.recent)+[(u'Delete recents...', self.del_recent)])))
  menu+=[(u'Screen mode', tuple(map(lambda x: (unicode(x.title())+u' (current)'*(appuifw.app.screen==x), lambda: appuifw.note(unicode(x))), ('full','large','normal'))))]
  menu+=[(u'Exit', self.exit)]
  for i in range(len(menu)):
   try:
    if menu[i][1]==[]: del menu[i]
    elif type(menu[i][1])==list:
     menu[i][1]=tuple(menu[i][1]); menu[i]=tuple(menu[i])
     if len(menu[i][1])==1: menu[i]=menu[i][1][0]
   except IndexError: break
  try: appuifw.app.menu=menu
  except TypeError: appuifw.note(u'Menu error', 'error')

 def traceback(self): import traceback; traceback.print_exc()
 def note_error(self, give_type=0, exc_value='Error'):
  if give_type: exc_type=str(sys.exc_type)+':\n'
  else: exc_type=''
  exc_value=str(sys.exc_value)
  appuifw.note(unicode(exc_type+exc_value),'error')
  self.refresh(); return 'error'
 def backup(self, content):
  x = r'C:\System\Temporary\TextEdit'
  if not os.path.exists(x): os.makedirs(x)
  open(x+r'\backup_save.txt','w').write(self.convert(content))

 def add_to_recents(self, entry=None):
  if entry:
   try:
    old=map(lambda x: x.lower(), self.recent).index(entry.lower())
    del self.recent[old]
   except ValueError: pass
   self.recent.insert(0, entry)
   if self.recents_len<len(self.recent): self.recent=self.recent[:self.recents_len]
  x = r'C:\System\Apps\TextEdit'
  if not os.path.exists(x): os.makedirs(x)
  open(x+r'\TextEdit.ini', 'w').write("self.recent = %s\n"%self.recent)
 def get_path(self, prompt):
  input_path=appuifw.query(unicode(prompt),'text',unicode(self.path))
  if input_path:
   self.path=input_path
   self.add_to_recents(input_path)
  return input_path

 def open(self):
  appuifw.app.title=u'Opening...'; appuifw.app.menu=[]
  e32.ao_sleep(0)
  try:
   cache=open(self.path).read()
   try: self.body.set(self.convert(cache, unicode, 1))
   except UnicodeError:
    appuifw.note(u'Some characters not displayed correctly','info',1)
    self.save_confirm=1
    try: self.body.set(self.convert(cache, appstdio.nice_unicode, 1))
    except (MemoryError, SymbianError): appstdio.memerr()
   else:
    self.body.set_pos(0)
    if len(cache)==len(self.body.get()): self.cache=self.body.get()
  except: return self.note_error()
  else: self.is_open=1
  self.refresh()
 def open_path(self, path):
  if self.close()==1: return
  self.path=path
  self.add_to_recents(self.path)
  self.open()
  self.refresh()
 def revert(self):
  if appuifw.query(u'Revert to saved?','query'): self.open()
 def open_as(self):
  if self.close()==1: return
  if self.get_path('Open:'): self.open()
 def del_recent(self):
  if appuifw.query(u'Select items to delete?','query'):
   while len(self.recent):
    i=appuifw.popup_menu(map(lambda x: unicode(os.path.split(x)[1]), self.recent), u'Delete recents:')
    if i>=0: del self.recent[i]
    else: break
   else: appuifw.note(u'Recents list empty')
   self.refresh()
   self.add_to_recents()

 def close(self):
  if not self.is_open and not self.body.get() in (u'', self.defaults['text']): self.is_open=2
  elif self.is_open==2 and self.body.get() in (u'', self.defaults['text']): self.is_open=0
  same = self.body.get()==self.cache
  if self.is_open and (same or appuifw.query(u'Close?','query')):
   if same or (not self.is_open and self.body.get() in (u'', self.defaults['text'])) or not self.save():
    appuifw.app.menu=[]; self.body.set_pos(0)
    self.body.set(self.defaults['text'])
    self.save_confirm=0
    self.is_open=0; self.refresh(); self.cache=None
  elif not self.is_open: return
  else: return 1
 def exit(self):
   if not self.close(): os.abort()
 def close_or_exit(self):
  if self.is_open==1 or not self.body.get() in (u'', self.defaults['text']): self.close()
  else: self.exit()

 def save(self, confirm=1, save_as=0):
  try:
   if self.wait or ((save_as or self.is_open!=1) and not self.get_path('Save as:')): return
   should_continue=1; self.wait=1
   if confirm or self.save_confirm:
    try:
     if os.path.exists(self.path): prompt="File exists.\nSave (replace)?"
     else: prompt="File doesn't exist.\nSave (make new)?"
    except UnicodeError: prompt="File may exist.\nSave?"
    should_continue=appuifw.query(unicode(prompt),'query')
  except: self.refresh(); return note_error()
  if should_continue:
   appuifw.app.title=u'Saving...'
   e32.ao_sleep(0); old_file=None; return1=None
   try:
    self.cache=self.body.get()
    self.backup(self.cache)
    if os.path.isfile(self.path): old_file=open(self.path).read()
    open(self.path,'w').write(self.convert(self.cache))
   except:
    return1=self.traceback()#.note_error()
    self.cache=None
    try:
     if old_file and appuifw.query(u'Error.\u2029Restore backup to file?','query'): open(self.path,'w').write(old_file)
    except : return1=self.traceback#.note_error()
   else:
    if appuifw.app.screen in ['large', 'full']: appuifw.note(u'Document saved','conf')
    self.is_open=1; self.cache=self.body.get()
    self.save_confirm=0
   self.refresh()
   return return1
  self.refresh()

 def memory_lock(self, focused=0):
  if focused: return
  screen=appuifw.app.screen
  appuifw.app.screen='normal'
  i=appuifw.selection_list([u'Continue',u'Exit'])
  appuifw.app.screen=screen
  if i==1: self.exit()
 def convert(self, x, type1=None, direction=0):
  if not type(x) in (str, unicode): return x
  if direction: x=x.replace('\n', '\n')
  else:  x=x.replace(u'\u2029', '\n')
  if type1: return type1(x)
  else: return x
 def nice_return(self):
  try:
   pos=self.body.get_pos()
   self.body.set(self.convert(self.body.get()))
   self.body.set_pos(pos)
  except: pass

 def input_print(self, input=None):
  try:
   if not input: input=appuifw.query(u'Word:','text',u'\t')
   text.body.set(unicode(input))
  except: note_error(1)

 def screen_mode(self, mode):
  appuifw.app.screen=mode
  print appuifw.app.screen
  self.refresh()
  print appuifw.app.menu[3][1][2]

 def position(self):
  appuifw.app.menu=[]; cur_pos=self.body.get_pos(); text=self.body.get(); i=0
  while i>=0:
   line_cur=text[:cur_pos].count(u'\u2029')+1
   line_tot=text.count(u'\u2029')+1
   char_cur=cur_pos
   char_tot=len(text)
   def format_words(text):
    text=text.replace(u'\u2029',u' ').replace(u'\t',u' ')
    text=text.split(' ')
    while text.count(' '): text.remove(' ')
    return len(text)
   word_cur=format_words(text[:cur_pos])
   word_tot=format_words(text)
   i=appuifw.popup_menu(map(lambda x: u'%s: %d/%d'%x, [('Line',line_cur,line_tot), ('Char',char_cur,char_tot), ('Word',word_cur,word_tot)]), u'Position')
   if i==1:
    input1=appuifw.query(u'Go to character:','number',char_cur)
    if input1>=0: self.body.set_pos(min(input1, len(text)))
   e32.ao_sleep(0)
   cur_pos=self.body.get_pos()
  self.refresh()

 def find(self, replace=0):
  appuifw.app.menu=[]; cur_pos=self.body.get_pos(); text=self.body.get()
  display=u''
  input_search, input_replace, input_search_replace = None, None, None
  def do_replace(cur_pos, text):
   e32.ao_sleep(0.2)
   self.body.set(text[:cur_pos]+text[cur_pos:cur_pos+len(self.search_str)].replace(self.search_str, self.replace_str)+text[cur_pos+len(self.search_str):])
   cur_pos=cur_pos+len(self.replace_str)-1
   self.body.set_pos(cur_pos)
   text=self.body.get()
   return cur_pos, text
  while 1:
   if not replace:
    input_search=appuifw.query(u'Find:'+display,'text',u'\u0000'+self.search_str)
    if input_search: self.search_str=input_search.replace(u'\u0000',u'')
    else: break
   elif replace==1 or (replace==2 and (not input_search or not input_replace)):
    input_search_replace=appuifw.query(u'Find / Replace with:'+display,'text',u'\u0000'+self.search_str+self.inputs_split+self.replace_str)
    if input_search_replace: input_search_replace=input_search_replace.replace(u'\u0000',u'').split(self.inputs_split)
    else: break
    if len(input_search_replace)==2: self.search_str, self.replace_str=input_search, input_replace=input_search_replace
    else:
     self.search_str=input_search_replace[0]
     if len(input_search_replace)==1: appuifw.note(u'No dividers found','error')
     elif len(input_search_replace)>2:
      appuifw.note(u'Too many dividers','error'); self.replace_str=u''
      for i in input_search_replace[1:]: self.replace_str+=i
     continue
   e32.ao_sleep(0.1)
   cur_pos+=1
   if len(text)<=cur_pos: cur_pos=len(text)
   pos=text[cur_pos:].find(self.search_str)
   if pos>=0:
    self.body.set_pos(cur_pos+pos)
    cur_pos+=pos
    if replace: cur_pos,text=do_replace(cur_pos, text)
   elif cur_pos>0:
    pos=text[:cur_pos].find(self.search_str)
    if pos>=0:
     self.body.set_pos(pos); cur_pos=pos
     if replace: cur_pos,text=do_replace(cur_pos, text)
     appuifw.note(u'Reached end of document, continued from top','info',1)
    else:
     appuifw.note(u'Not found','error')
     if replace==2: break
   total_found=text.count(self.search_str)
   if appuifw.app.screen in ('large','full'): display=u'\u2029(%d/%d)'%((total_found!=0)+text[:cur_pos].count(self.search_str), total_found)
   appuifw.app.title=u'Find: %d/%d'%((total_found!=0)+text[:cur_pos].count(self.search_str), total_found)
  self.refresh()
