import appuifw, key_codes, e32, audio

prefix=r'E:\Documents\Python\Sound\Sounds'+'\\'
S = [
 audio.Sound.open(prefix + "c.mid"),
 audio.Sound.open(prefix + "d.mid"),
 audio.Sound.open(prefix + "e.mid"),
 audio.Sound.open(prefix + "f.mid"),
 audio.Sound.open(prefix + "f.mid"),
  ]

def playsC(): S[0].play(1,0)
def keys(event):
    if event['keycode'] == key_codes.EKey1: playsC()

def quit():
    for x in S: x.close()
    app_lock.signal()
    #appuifw.app.set_exit()

appuifw.app.body = canvas =appuifw.Canvas(event_callback=keys)
appuifw.app.title = u"Sound"
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()
