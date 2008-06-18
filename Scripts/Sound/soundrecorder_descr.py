# Copyright (c) 2006 Jurgen Scheible
# Sound recording / playing script 

import appuifw, e32
# import the audio module
import audio
# define a name of the file to be the sound file, incl. its full path
filename = r'E:\Sounds\Digital\Sound clip.amr'

# define the recording part:
def recording():
    global S
    # open the sound file to be ready for recording and set an instance (S) of it
    S=audio.Sound.open(filename)
    # do the recording (has to be stopped by closing() function below)
    S.record()
    print "Recording on! To end it, select stop from menu!"

# define the playing part:
def playing():
    global S
    try:
        # open the sound file to be ready for playing by setting an instance (S) of it
        S=audio.Sound.open(filename)
        # play the sound file
        S.play()
        print "Playing"
    except:
        print "Record first a sound!"

# stopping of recording / playing and closing of the sound file
def closing():
    global S
    S.stop()
    S.close()
    print "Stopped"

def quit():
    script_lock.signal()
    #appuifw.app.set_exit()

# define the application menu
appuifw.app.menu = [(u"play", playing),
                    (u"record", recording),
                    (u"stop", closing)]

appuifw.app.title = u"Sound recorder"

appuifw.app.exit_key_handler = quit
script_lock = e32.Ao_lock()
script_lock.wait()
