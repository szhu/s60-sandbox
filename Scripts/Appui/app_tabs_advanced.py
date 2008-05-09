# Copyright (c) 2006 Jurgen Scheible
# This script creates tabs that let you switch between different applications
# listbox app, listbox app and canvas app


import appuifw
import e32
from graphics import *


# define application 1: listobx app

# create your icons for the listbox content  
icon1 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 28, 29)
icon2 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 40, 41)
icon3 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 30, 31)
icon4 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 32, 33)
icon5 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 34, 35)
icon6 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 36, 37)
icon7 = appuifw.Icon(u"z:\\system\\data\\avkon.mbm", 38, 39)

# create your content list of your listbox including the icons to be used for each entry
entries = [(u"Signal", icon1),
           (u"Battery", icon2),
           (u"Sirene", icon3),
           (u"Waste", icon4),
           (u"Helicopter", icon5),
           (u"Train", icon6),
           (u"Auto", icon7)]

# create the listbox callback handler
def handler():
    print "done"
    
# create an instance of appuifw.Listbox(), include the content list "entries" and the callback function "handler"
app1 = appuifw.Listbox(entries,handler)



# define application 2: listbox app

# define the list of items as pop-up menu content
L2 = [u"Stefan", u"Holger", u"Emil", u"Ludger"]

# create the listbox callback handler
def handler_L2():
    print "ola"

# create the pop-up menu 
app2 = appuifw.Listbox(L2, handler_L2) 



# define application 3: canvas application

def app_3():
    global canvas
    img=Image.new((176,208))
    img.line((20,20,20,120),0xff00ee)
    img.rectangle((40,60,50,80),0xff0000)
    img.point((50.,150.),0xff0000,width=40)
    img.ellipse((100,150,150,180),0x0000ff)
    img.text((100,80), u'hello')
    
    # define your redraw function (still belonging to app 3) 
    def handle_redraw(rect):
    #global canvas
        canvas.blit(img)
    # define the canvas, include the redraw callback function
    canvas =appuifw.Canvas(event_callback=None, redraw_callback=handle_redraw)
    appuifw.app.body = canvas

    

def exit_key_handler():
    app_lock.signal()

# create a tab handler that switches the application based on what tab is selected
def handle_tab(index):
    global lb
    if index == 0:
        appuifw.app.body = app1 # switch to application 1
    if index == 1:
        appuifw.app.body = app2 # switch to application 2
    if index == 2:
        app_3() # switch to application 3

    
# create an Active Object
app_lock = e32.Ao_lock()

# create the tabs with its names in unicode as a list, include the tab handler
appuifw.app.set_tabs([u"One", u"Two", u"Three"],handle_tab)

# set the title of the script
appuifw.app.title = u'Tabs advanced'

# set app.body to app1 (for start of script)
appuifw.app.body = app1


appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()