import appuifw, e32
select_list=[u'Menu: Backup',u'Menu: Restore']
i=appuifw.popup_menu(select_list)
if not appuifw.query(u'Confirm\n'+select_list[i],'query'): i=None
if i in (0,1):
 import appswitch
 dirs=r'E:\Backup\OS\Applications.dat',r'C:\System\Data\Applications.dat'
 if u'Menu' in appswitch.application_list(0):
  m = appuifw.popup_menu([u'End',u'Kill'],u'Menu')
  if m==0: appswitch.end_app(u'Menu')
  if m==1: appswitch.kill_app(u'Menu')
 if i==0: e32.file_copy(dirs[0],dirs[1])
 if i==1: e32.file_copy(dirs[1],dirs[0])
if i>=0: appuifw.note(u'Done\n'+select_list[i],'conf')
