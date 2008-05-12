# Copyright (c) 2006 Jurgen Scheible
# Application skeleton (no main loop)

import appuifw
import e32

appuifw.app.screen='large'

 
# create your application logic ...


def item1():
    print "hello"

def subitem1():
    print "aha"

def subitem2():
    print "good"

appuifw.app.menu = [(u"item 1", item1),
                    (u"Submenu 1", ((u"sub item 1", subitem1),
                                    (u"sub item 2", subitem2)))]

def exit_key_handler():
    app_lock.signal()

appuifw.app.title = u"drawing"    
 
app_lock = e32.Ao_lock()

#appuifw.app.body = ... 

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()




""" description:


# 1. import all modules needed
import appuifw
import e32

# 2. set the screen size to large
appuifw.app.screen='large'


 
# 3. create your application logic ...
# e.g. create all your definitions (functions) or classes and build instances of them or call them etc.
# ...... application logic ....




# 4. create the application menu including submenus
# create the callback functions for the application menu and its submenus
def item1():
    print ""
    round.set(u'item one was selected')

def item1():
    print "hello"

def subitem1():
    print "aha"

def subitem2():
    print "good"

appuifw.app.menu = [(u"item 1", item1),
                    (u"Submenu 1", ((u"sub item 1", subitem1),
                                    (u"sub item 2", subitem2)))]
    


# 5. create and set an exit key handler
def exit_key_handler():
    app_lock.signal()

# 6. set the application title
appuifw.app.title = u"drawing"    

# 7. crate an active objects 
app_lock = e32.Ao_lock()

# 8. set the application body 
appuifw.app.body = ... 

# no main loop

appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()

"""