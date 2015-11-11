s60-sandbox
===========

Some applications for Symbian S60.


Contents & History
------------------

Writing Python code on a Nokia 3650 was my first real attempt at Python – and programming, for that matter. This repo contains the culmination of my programming work from around 2006 to 2008.

Nokia developed a Python platform for its S60 phones, called [Python for S60][], and that is what I developed on.

This repo contains:

 - [**Filebrwser/**](Filebrwser)  
   A file browser. Included with PyS60 as a script; I turned it into an app and added improvements.

 - [**PyInstaller/**](PyInstaller)  
   Converts Python scripts into native apps. Included with PyS60; I improved the UI.

 - [**Python/**](Python)  
   Runs Python scripts. Included with PyS60; I added improvements.  
   [**Python/A/**](Python/A) and [**Python/B/**](Python/B) contain some scripts.

 - [**TextEdit/**](TextEdit)  
   A plain-text editor a variety of editing features. I created this one myself entirely and used it as a bootstrap to write more code. Sorry for the name theft, fruit company, but I thought it was a good one.

 - [**Scripts/**](Scripts)  
   More scripts.


Some extra notes:

**Code style.** This code is insanely lacking both horizontal and vertical whitespace. The reason for this is that I wrote all of it not on a computer but on the phone itself, so I was working with a screen width of about 20 characters wide and a cursor that could move only one character at a time.

**Other's work.** Some parts of the code here are not mine; it should be very obvious which parts. I've included them too for the sake of completeness, and also because Nokia probably no longer cares about whatever copyright it has on S60-related things.

**Commit convention.** Each commit on the `original` branch adds the most recent version of each file from before 2015. The author date reflects the last modified time.

**Future plans.** For fun, I may generate screenshots or modernize this 7-year-old code in the next few months.


Compatibility
-------------

These apps are written in Python and require the [Python for S60][] runtime to work.

The `.py` files should work on all PyS60 variants, but the binaries are likely S60v1-only. As stated above, PyS60 comes with an app (PyInstaller) that can turn Python scripts into native apps. (This is how the TextEdit app binaries were generated.)

[Python for S60]: https://en.wikipedia.org/wiki/Python_for_S60
