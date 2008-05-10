# Copyright (c) 2006 Jurgen Scheible
# This script performs a query with a single-field dialog (text input field)
# and lets the phone speak out the text (text to speech) that the users have typed in

# NOTE: this script runs only with Python S60 version 3.1.14 or above
# NOTE: this script doesn't work on all S60 phones neccessarily. Check your phone model if it has text to speech capability at all


# import the module called audio
import appuifw
import audio

# trigger a text input-field to let the user type a word
text = appuifw.query(u"Type few words:", "text")
# the phone speaks out the text that you have just typed (you can hear it through the loudspeakers of your phone)
audio.say(text)