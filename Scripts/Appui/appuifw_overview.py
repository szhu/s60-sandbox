# Copyright (c) 2006 Jurgen Scheible
# Script that creates a application menue to select all possible
# appuifw functions to see how they appear

import appuifw
import e32

# define the functions:


# note (3 different types are possible) 
def note_info(): # type: info 
   # create a pop-up note: appuifw.note(label, type)    
   appuifw.note(u"Hello", "info")
   
def note_error(): # type: error  
   appuifw.note(u"file not found", "error")
   
def note_conf(): # type: conf   
   appuifw.note(u"upload done", "conf")
   

# query
def query_text():
    # create a single-field dialog (text input field):  appuifw.query(label, type)
    data = appuifw.query(u"Type a word:", "text")
    print data

def query_number():
    # create a single-field dialog (number input field):  appuifw.query(label, type)
    data = appuifw.query(u"Type a number:", "number")
    print data

def query_date():
    # create a single-field dialog (date input field):  appuifw.query(label, type)
    data = appuifw.query(u"Type a date:", "date")
    print data

def query_time():
    # create a single-field dialog (time input field):  appuifw.query(label, type)
    data = appuifw.query(u"Type a time:", "time")
    print data

def query_code():
    # create a single-field dialog (code input field):  appuifw.query(label, type)
    data = appuifw.query(u"Type a code:", "code")
    print data

def query_question():
    # create a single-field dialog (question):  appuifw.query(label, type)
    if appuifw.query(u"Are you ok:", "query") == True:
        print "you pressed ok"
    else:
        print "you pressed cancel"       


# multi_query
def multi_query():
    # create a double-field dialog (text input field):  appuifw.multi_query(label1, label2)
    data1,data2 = appuifw.multi_query(u"Type your first name:",u"Type your surname:")
    print data1
    print data2
    

# popup_menu
def popup_menu():
    # create a list as content for the menu
    L = [u"Stefan", u"Holger", u"Emil"]
    # create the popup menu: appuifw.popup_menu(list, label)
    test = appuifw.popup_menu(L, u"Select + press OK:") 
    if test == 0 : # 0 refers to the first entry in the list L
        print "Stefan was selected"
    if test == 1 : # 1 refers to the second entry in the list L
        print "Holger was selected"
    if test == 2 : # 2 refers to the third entry in the list L
        print "Emil was selected"     



# selection_list
def selection_list():
    # define the list of items
    L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']
    # create the selection list: appuifw.selection_list(list , search_field=1 or 0)
    index = appuifw.selection_list(L , search_field=1)
    # use the result of the selection to trigger some action (here we just print something)
    if index == 0:
        print "cakewalk was selected"
    else:
        print "thanks for choosing"


# - multi_selectionlist: with checkbox
def  multi_selectionlist_checkbox():
    # define the list of items
    L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']
    # create the multi-selection list with checkbox
    index = appuifw.multi_selection_list(L , style='checkbox', search_field=1)

# - multi_selectionlist: with checkmark
def  multi_selectionlist_checkmark():
    # define the list of items 
    L = [u'cakewalk', u'com-port', u'computer', u'bluetooth', u'mobile', u'screen', u'camera', u'keys']
    # create the multi-selection list with checkmark
    tuple = appuifw.multi_selection_list(L , style='checkmark', search_field=1)


# define an exit key handler
def exit_handler():
    lock.signal()   # .signal releases the Active Object 

# set an Active Object (needs to be done for application menus)
lock=e32.Ao_lock()

# create the application menu
appuifw.app.menu=[
    (u'multi_query',multi_query),
    (u'popup-menu',popup_menu),    
    (u'selection_list',selection_list),
    (u'checkbox: multi_list',multi_selectionlist_checkbox),
    (u'checkmark: multi_list',multi_selectionlist_checkmark),
    (u'Exit',lock.signal),
    (u'note info',note_info),
    (u'note error',note_error),
    (u'note conf',note_conf),
    (u'query text',query_text),
    (u'query number',query_number),
    (u'query date',query_date),
    (u'query time',query_time),
    (u'query code',query_code),
    (u'query query',query_question)] 


appuifw.app.body = appuifw.Text(u'press options')

# define what shall happen it the exit button is pressed
appuifw.app.exit_key_handler=exit_handler

lock.wait()