project=1

import appuifw, e32
if appuifw.query(u'Clear screen?','query'): appuifw.app.body.clear()
def exit(): appuifw.app.exit_key_handler.running=0
appuifw.app.exit_key_handler=exit
appuifw.app.exit_key_handler.running=1
def refresh(title=None, title_append=u''):
 appuifw.app.title=u'Contacts %s:\n'%project+(title or u'%s / %s'%(str(i).zfill(len(contacts_len_str)), contacts_len_str) + title_append)
 e32.ao_sleep(0.0)
 return appuifw.app.exit_key_handler.running
refresh(u'Importing...')
import contacts; i=0
ContactsDb=contacts.ContactsDb().items()
contacts_len_str=str(len(ContactsDb))

for (contactno, contact) in ContactsDb:
 if not refresh(): break
 if project==3: is_found=0; field_types=[]
 if project in (1, 2): last_name_no=None; first_name_no=None
 if project==1: found_info=''
 i2=0

 for fieldno in contact.keys():
  if not refresh(title_append=u' '+u'.'*i2): break
  field=contact[fieldno]
  if project==3:
   field_types+=[field.type]
   is_found=1
   if is_found:
    print repr(field.type), repr(field.location)
    if field.type=='po_box': field.type#='po_box'
  if project in (1, 2):
   if field.type=='last_name': last_name_no=fieldno#; print 'Last: '+field.value
   if field.type=='first_name': first_name_no=fieldno#; print 'First: '+field.value
  if project==1:
   import appstdio
   if field.type=='phone_number' and field.location!='none':
    if field.label in ('Telephone (%s)'%field.location, 'Tel. (%s)'%field.location):
     found_info += ' '+field.location+' -> '
     field.label=field.location.title()
     found_info += appstdio.nice_str(field.label)+'\n'
  i2+=1

 if project==3:
  if is_found:
   if 'last_name' in field_types:
    print contact[field_types.index('last_name')].value,
   if 'first_name' in field_types:
    print contact[field_types.index('first_name')].value
   else: print ''
 if project==2:
  if last_name_no!=None and first_name_no==None:
   if contact[last_name_no].value in ('Zhu', 'Wu', 'Song, Fang'):
    contact[last_name_no].label='Last name'
   else: contact[last_name_no].label='Name'
   print contact[last_name_no].value+' -> '+contact[last_name_no].label
 if project==1:
  if found_info:
   if last_name_no>=0: print contact[last_name_no].value,
   if first_name_no>=0: print contact[first_name_no].value
   else: print ''
   print found_info.rstrip()
 i+=1

if refresh(): appuifw.note(u'Done','conf')
else: appuifw.note(u'Cancelled')
