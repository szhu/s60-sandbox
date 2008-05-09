

import e32,socket,appuifw

def bt_send():
    file=(u'e:\\Images\\picture1.jpg')
    device=socket.bt_obex_discover()
    print 'device:', device 
    address=device[0]
    print 'address:', address 
    channel=device[1][u'OBEX Object Push']
    print 'channel:', channel 
    socket.bt_obex_send_file(address,channel,file)
    appuifw.note(u"Picture sent","info")

def quit():
    app_lock.signal()

print 'press options to start' 

app_lock = e32.Ao_lock()
appuifw.app.title = u"Bluetooth photo send"
appuifw.app.menu = [(u"Start", bt_send),(u"Exit",quit)]
app_lock.wait()