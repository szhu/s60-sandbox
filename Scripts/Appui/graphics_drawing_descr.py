# Copyright (c) 2005 Jurgen Scheible
# Graphics drawing
# use button Arrow up,down,left,right, to move the colour point

import appuifw
from appuifw import *
import e32
from key_codes import *
# use this to get your graohics stuff in
from graphics import *


class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            code=event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code,0)+1
            self._keyboard_state[code]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False

keyboard=Keyboard()



def quit():
    global running
    running=0
    appuifw.app.set_exit()


appuifw.app.screen='full'
# create an empty image (appears as white image)
img=Image.new((176,208))
# defien the blobsize and starting x,y coordinates of the point on the canvas
blobsize=30
location_x = 100.
location_y = 100.

# define a function that redraws the screen, in this case the image shall be
# drawn again and again (use the .blit function for this)
def handle_redraw(rect):
    canvas.blit(img)

running=1

# define the canvas and include the redraw function as callback, and also the key scanning function (keyboard.handle_event)
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=handle_redraw)
# set the application body as canvas
appuifw.app.body=canvas

app.exit_key_handler=quit

# create a loop to define stuff in it that needs to be run through again and again
while running:
    # clear the image (put as a white image)
    img.clear(0x0000ff)
    # define a point and add it to the image, define its: current x,y coordinate, and its colour and size
    img.point((location_x + blobsize/2,location_y + blobsize/2),0xff0000,width=blobsize)
    # redraw the image
    handle_redraw(())
    # this is needed to start a short scheduler to allow checking for key events
    e32.ao_yield()
    # if left arrow key is pressed, change the x coordinate of the point by 1 dot
    if keyboard.is_down(EScancodeLeftArrow):
        location_x = location_x - 1

    if keyboard.is_down(EScancodeRightArrow):
        location_x = location_x + 1

    # if down arrow key is pressed, change the y coordinate of the point by 1 dot
    if keyboard.is_down(EScancodeDownArrow):
        location_y = location_y + 1


    if keyboard.is_down(EScancodeUpArrow):
        location_y = location_y - 1






        


 



