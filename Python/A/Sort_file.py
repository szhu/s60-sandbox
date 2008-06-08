import appuifw, appstdio, graphics, e32, os
class restore:
 def __init__(self):
  logs_base=r'C:\Logs'
  if not os.path.exists(logs_base): os.mkdir(logs_base)
  self.dirs_log=open(logs_base+r'\dirs.log','w')
  self.files_log=open(logs_base+r'\files.log','w')
  self.software_log=open(logs_base+r'\software.log','w')
  if not os.path.exists(r'E:\Restore\Unknown'): os.mkdir(r'E:\Restore\Unknown')
  self.python_log=open(logs_base+r'\python.log','w')
  self.running=1
  self.upmost=r'E:\Restore\Restore'
  self.dir_list=[self.upmost]
  self.canvas=appuifw.Canvas()
  self.img=graphics.Image.new(self.canvas.size)
  self.run()
 class lists:
  txt=[]; software=[]
 class filters:
   def text(self, x):
     return x[-4:].lower()=='.txt' and not os.path.isdir(x)
   def software(self, x):
     if not self.text(x): return 0
     try: file_contents=open(x).read()
     except MemoryError: return 2
     if (
      file_contents.find('Copyright (c) 2005 Nokia Corporation')>=0 and
      (file_contents.find("'''")>=0 or
      file_contents.find('"""')>=0 or
      file_contents.find('\n#')>=0)):
       return 1
     return 0
 filters=filters()

 def exit(self): self.running=0

 def run(self):
  dirs_scanned=0; files_scanned=0; total_dirs=1
  appuifw.app.body=self.canvas
  appuifw.app.exit_key_handler=self.exit

  while len(self.dir_list):
   folder_files_scanned=0
   dir_index=0; cur_dir=self.dir_list[0]
   dir_contents=map(lambda x: self.dir_list[0]+'\\'+x, os.listdir(cur_dir))
   for i in range(len(dir_contents)):
    cur_path=dir_contents[i]
    self.img.clear()
    self.img.text((5,15),u'Dirs: %d / %d'%(dirs_scanned, total_dirs))
    self.img.text((5,28),u'Files in dir: %d / %d'%(folder_files_scanned, len(dir_contents)))
    self.img.text((5,75),u'Text: %d'%len(self.lists.txt))
    self.img.text((5,88),u'Software: %d'%len(self.lists.software))
    try:
     self.img.text((5,45),unicode(self.dir_list[0]), 0, u'LatinPlain12')
     self.img.text((5,58),unicode(cur_path[cur_path.rfind('\\')+1:]), 0, u'LatinPlain12')
    except UnicodeError:
     self.img.text((5,45),appstdio.nice_unicode(self.dir_list[0]), 0, u'LatinPlain12')
     self.img.text((5,58),appstdio.nice_unicode(cur_path[cur_path.rfind('\\')+1:]), 0, u'LatinPlain12')
    self.canvas.blit(self.img)

    if os.path.isdir(cur_path):
     if dir_index==-1: self.dir_list=[cur_path]+self.dir_list
     else: self.dir_list+=[cur_path]
     total_dirs+=1

    if self.filters.text(cur_path):
     self.lists.txt+=[1]#[cur_path]
     self.img.text((90,75),u'Detected')
    if self.filters.software(cur_path)==2:
     self.img.text((90,88),u'MemoryError',0xf00000)
    elif self.filters.software(cur_path):
     self.lists.software+=[0]#[cur_path]
     #try: os.rename(cur_path, r'E:\Restore\Unknown' + cur_path[cur_path.rfind('\\'):])
     try: appuifw.Content_handler().open_standalone(cur_path); appuifw.selection_list([])
     except OSError:
      if not appuifw.query(u'OSError','query'): self.exit()
     self.img.text((90,88),u'Detected')

    self.canvas.blit(self.img)
    self.files_log.write(cur_path+'\n')
    files_scanned+=1
    folder_files_scanned+=1
    e32.ao_sleep(0)
    if not self.running: break
   dirs_scanned+=1
   self.dirs_log.write(self.dir_list[0]+'\n')
   del self.dir_list[self.dir_list.index(cur_dir)]
   if not self.running: break
  while self.running:
   self.img.text((90,135),u'Done',0x008000, u'Alb17')
   self.canvas.blit(self.img)
   e32.ao_sleep(0)
restore()
