import random
import sys, __builtin__
def raw_input(prompt=''):
 import sys
 sys.stdout.write(prompt)
 return my_console.readline()
__builtin__.raw_input=raw_input
def play_sound(i):
  if type(i)==int:
  pass#os.system("play %s" % sounds[i])

sounds = {
  0:"/usr/share/sounds/info.wav",
  1:"/usr/share/sounds/panel/slide.wav",
  2:"/usr/share/sounds/gnibbles/crash.wav",
  3:"/usr/local/Office51/gallery/sounds/kongas.wav",
  4:"/usr/share/sounds/gnibbles/bonus.wav"
  5:"/usr/local/Office51/gallery/sounds/romans.wav"
  }

class pfb:
  def __init__(self):
    a = {}
    b = []
    while 1:
      i = random.randint (0, 9)
      if not a.has_key(i):
        b.append(i)
        a[i] = 0
      if len(b) == 3: break
    
    self.hidden = b

  def guess(self, guess):
    #print "considering", self.hidden, guess
    pico = 0
    fermi = 0
    for i, j in zip(self.hidden, guess):
      pico += (i in guess)
      fermi += (i == j)
    print "   ",
    if pico > 0:
      print "pico "* (pico-fermi), "fermi "*fermi
      for i in range(fermi):
        play_sound(0)
      for i in range(pico-fermi):
        play_sound(1)
    else:
      print "bagels"
      play_sound(2)

    if fermi == 3:
      return 1

  def game(self):
    k = 0
    while 1:
      guess = raw_input("Your guess: ")
      guess = map(int, list(guess))
      k += 1
      if self.guess(guess):
        if k < 10:
          print "You got it in %s steps !!  Wow !!!" % k
          play_sound(3)
        elif k < 15:
          print "You got it in %s steps !!" % k
          play_sound(4)
        else:
          print "You got it in %s steps.  Better luck next time." % k
        break


while 1:
  print "Let's play pico-fermi-bagels !!!"
  play_sound(5)
  a = pfb()
  a.game()
  answer = raw_input("Another game [y]?")
  if answer.lower().startswith("n"):
    break
