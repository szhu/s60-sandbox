# Copyright (c) 2006 Jurgen Scheible
# This script performs a query with a single-field dialog (text input field)
# and lets the phone speak out the text (text to speech) that the users have typed in
# NOTE: this script runs only with Python S60 version 3.1.14 or above
# NOTE: this script doesn't work on all S60 phones neccessarily. Check your phone model if it has text to speech capability at all

import appuifw
import audio

text = appuifw.query(u"Type a word:", "text")
audio.say(text)
