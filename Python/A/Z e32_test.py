import e32, appuifw, os
class test:
 def exit1(self): 
  self.running=0
 def __init__(self):
  self.running=1; last=None
  appuifw.app.menu=[(u'Stop',self.exit1)]
  i=0
  while self.running:
   cur=str(e32._mem_info()[:3])
   if cur!=last or 1: os.write(0 ,'\n'+cur)
   last=cur
   e32.ao_sleep(0)
   i+=1
test()