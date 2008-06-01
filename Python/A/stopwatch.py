import appuifw, time, e32, os
class stopwatch:
 running=1
 def exit1(self): self.running=0
 def __init__(self):
  appuifw.exit_key_handler=self.exit1
  start=time.clock()
  while self.running:
   #e32.ao_sleep(0)
   os.write(0,'\n %f'%(time.clock()-start))

stopwatch()
