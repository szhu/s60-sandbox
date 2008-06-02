import appuifw, e32
appuifw.app.body.clear()
print 'Hello.'
e32.ao_sleep(1)
x = appuifw.multi_query(u"What's your:\nFirst name?",u"Last name?")
if x: appuifw.note('Hello, %s. %s.'%(x[0][0].capitalize(), x[1][0].capitalize()))
print 'Goodbye.'
e32.ao_sleep(2)
appuifw.app.body.clear()
