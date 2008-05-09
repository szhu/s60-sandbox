import e32, camera, appuifw, key_codes

def finder_cb(im):
    canvas.blit(im)

def take_picture():
    camera.stop_finder()
    pic = camera.take_photo(size = (640,480))
    w,h = canvas.size
    canvas.blit(pic,target=(0, 0, w, 0.75 * w), scale = 1)
    pic.save('e:\\Images\\picture1.jpg')

def quit():
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas

camera.start_finder(finder_cb)
canvas.bind(key_codes.EKeySelect, take_picture)

appuifw.app.title = u"My Camera"
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()


