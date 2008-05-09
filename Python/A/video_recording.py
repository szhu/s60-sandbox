#  Video recording application
# (c) Copyright 2007 Jurgen Scheible under terms of GPL
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


import e32, camera, appuifw, key_codes, os

control_light=0
videodir=u"e:\\pyvideos\\"

try:
    if not os.path.exists(videodir):  
        os.makedirs(videodir)
    else:
        pass
except:
    appuifw.note(u"Problems creating directory on memorycard", "info")  

def finder_cb(im):
    global control_light
    if control_light==1:
        im.point((20, 20), outline = (255, 0, 0), width = 25) 
    else:
        im.point((20, 20), outline = (0, 255, 0), width = 25) 
    canvas.blit(im)

def video_callback(err,current_state):
    global control_light   
    if current_state == camera.EPrepareComplete:
        control_light=1
    else:
        pass 

def start_video():
    files=os.listdir(videodir)
    num = len(files) 
    filename = videodir+'pyvideo'+unicode(num+1)+'.3gp'
    canvas.bind(key_codes.EKeySelect, stop_video)
    camera.start_record(filename,video_callback)       
    
def stop_video():
    global control_light
    control_light = 0    
    camera.stop_record()
    canvas.bind(key_codes.EKeySelect, start_video)

def quit():
    camera.stop_finder()
    camera.release()
    app_lock.signal()

canvas = appuifw.Canvas()
appuifw.app.body = canvas

camera.start_finder(finder_cb)
canvas.bind(key_codes.EKeySelect, start_video)

appuifw.app.title = u"Video RECORDER"
appuifw.app.exit_key_handler = quit
app_lock = e32.Ao_lock()
app_lock.wait()