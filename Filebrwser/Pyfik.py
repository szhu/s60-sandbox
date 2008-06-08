# Pyfik 0.2
# Author : Shrim (dimonvideo.ru) 
# cyke64 (english translation)

import appuifw,e32,os
from appuifw import *
from graphics import *
def sort(s):
 f,d=[],[]
 for i in range(0, len(s)):
  if os.path.isdir(dir+s[i])==1:d.append(s[i])
  else:f.append(s[i])
 return d+f
def up():
 global p,d
 l=len(f)
 if p>0:p-=1
 elif d>0:d-=1
 elif l>14:p,d=14,l-15
 elif l>0:p=l-1
 run()
def down():
 global p,d
 l=len(f)
 if l>14:
  if p<14:p+=1
  elif p+d+1<l:d+=1  
  else:p,d=0,0
 elif l>0:
  if p+1<l:p+=1
  else:p,d=0,0
 run()
def go():
 global dir,f,p,i,d
 if len(f)>0:
  if os.path.isdir(dir+f[p+d])==1:
   ff=os.listdir(dir+f[p+d])
   if len(ff)>0:
    dir+=f[p+d]+'/'
    f,p,i,d=sort(ff),0,0,0
    run()
def back():
 global dir,f,p,i,d
 if len(dir)>3:
  z=os.path.dirname(dir)
  w=(os.path.split(z))[1]
  z=os.path.dirname(z)
  if len(z)>3:dir=z+'/'
  else:dir=z
  f=os.listdir(dir)
  f=sort(f)
  p,i,d=0,0,0
  while len(f)>p:
   if f[p]==w:break
   else:p+=1
  if p>14:d,p=p-14,14
 else:dir,f,p,i,d='',['c:','d:','e:','z:'],0,0,0
 run()
def start():
 try:
  n=os.path.normpath(dir+f[p+d])
  if os.path.isfile(n):
   if n[-4:]=='.app':
    try:e32.start_exe('z:\\system\\programs\\apprun.exe',n)
    except:None
   else:
    try:Content_handler().open_standalone(n)
    except:None
  else:go()
 except:None
def ru(x):
 t=x.decode('utf-8')
 return t
app.screen='full'
img=Image.new((176,208))


canvas=appuifw.Canvas()
app.body=canvas
app.exit_key_handler=app.set_exit
canvas.bind(63497,up)
canvas.bind(63498,down)
canvas.bind(63496,go)
canvas.bind(63495,back)
canvas.bind(63557,start)
dir,f,p,i,d='',['C:','D:','E:','Z:'],0,0,0
def run():
 global i
 fpd,dfpd,p12=f[p+d],dir+f[p+d],12*p
 rfpd,rdfpd=ru(fpd),ru(dfpd)
 img.clear(0xf0f0e0)
 img.line((0,13,176,13),0x808080)
 img.line((0,194,176,194),0x808080)
 if len(rdfpd)<31:txt=rdfpd
 elif len(rfpd)<28:txt=ru(dir[:28-len(rfpd)]+'... /'+fpd)
 else:txt=rfpd[-30:]
 img.text((3,11),txt,fill=0x303030,font=u'alp13')
 img.text((5,206),u'Pyfik 0.2',fill=0x303030,font=u'latinbold12')
 img.text((130,206),u'Exit',fill=0x303030,font=u'latinbold12')
 img.polygon((0,14+p12,176,14+p12,176,25+p12,0,25+p12),0x3030ff,0x3030ff)
 if len(f)>15:
  img.polygon((170,14,175,14,175,193,170,193),0x808080,0xf0f0f0)
  q=15+int(177.0/len(f)*d)
  qp=q+int(177.0/len(f)*15)+1
  img.polygon((171,q,174,q,174,qp,171,qp),0x505050,0x505050)
 while i<15:
  try:
   fid,dfid,i12=f[i+d],dir+f[i+d],12*i
   rfid,rdfid,i1224=ru(fid),ru(dfid),24+i12
   if len(rfid)<20:txt=rfid
   else:txt=rfid[:18]+'...'
   if len(dfid)==2:
    img.polygon((3,18+i12,6,15+i12, 6,15+i12,13,15+i12, 13,i1224,3,i1224),0x505050,0xa0a0a0)
    img.text((18,24+i12),rfid,fill=0x303030,font=u'alp')
   elif os.path.isdir(dfid)==1:
    img.polygon((3,16+i12,4,15+i12,4,15+i12,8,15+i12,9,16+i12,12,16+i12,12,16+i12,13,17+i12,13,i1224,3,i1224),0x707070,0xffff0f)
    if len(os.listdir(dfid))>0:img.text((5,i1224),'+  '+txt,fill=0x303030,font=u'LatinPlain12')
    else:img.text((5,i1224),'-  '+txt,fill=0x303030,font=u'LatinPlain12')
   elif os.path.isfile(dfid)==1:
    img.polygon((3,15+i12,10,15+i12,10,15+i12,13,18+i12,13,i1224,3,i1224),0x808080,0xd0d0d0)
    w=os.path.getsize(dfid)
    if w>=1048576:txt+=" '"+str(w/1048576)+"Mb'"
    elif w>=1024:txt+=" '"+str(w/1024)+"kb'"
    else:txt+=" '"+str(w)+"b'"
    img.text((18,24+i12),txt,fill=0x303030,font=u'alp')
   i+=1
  except:break
 if len(f)>15:i-=15
 else:i-=len(f)
 canvas.blit(img)
run()
while 1:e32.ao_yield()