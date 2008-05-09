# Copyright (c) 2005 Jurgen Scheible
# script that connects to the serial port of the PC
# and lets you send characters to the PC

import appuifw
# import the module socket
import socket
import e32

# function that handles the bluetooth connection:
def bt_connect():
    global sock
    # create a bluetooth socket
    sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    target=''# here you can give the bt address of the other mobile if you know it
    if not target:
        # scan for bluetooth devices
        address,services=socket.bt_discover()
        print "Discovered: %s, %s"%(address,services)
        if len(services)>1:
            choices=services.keys()
            choices.sort()
            # bring up a popup menu and show the available bt devices for selection
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                        for x in choices],u'Choose port:')
            target=(address,services[choices[choice]])
        else:
            target=(address,services.values()[0])
    print "Connecting to "+str(target)
    # connect to the serial port of the PC
    sock.connect(target)
    print "OK."

    # call the text input field function   
    bt_typetext()
        
# define the textinput function
def bt_typetext():
    global sock
    # create the text input field
    test = appuifw.query(u"Type words", "text", u"")
    # if cancel has been pressed, then quit the application otherwise send the character over bluetooth
    if test == None:
        exit_key_handler()
    else:
        # send the typed in characters over bluetooth to the PC
        sock.send(test)
        # call again the textinput field function to show the text input again
        bt_typetext()

def exit_key_handler():
    script_lock.signal()
    appuifw.app.set_exit()

appuifw.app.title = u"bt mob to PC"

script_lock = e32.Ao_lock()

appuifw.app.exit_key_handler = exit_key_handler()

# call the function that handles the bluetooth connection
bt_connect()

script_lock.wait()


