import platform
import json
import copy
import operator

if platform.system() == 'Darwin':
  from MockLedStrip import LedStrip_WS2801
else:
  from vendor.LedStrip_WS2801 import LedStrip_WS2801

class LedManager:
  def __init__(self):
    self.ledCount = 25
    self.ledStrip = LedStrip_WS2801(self.ledCount)

    self.timeScale = 1

    self.currentColor = [0,0,0]

    self.tweenFrom           = copy.copy(self.currentColor)
    self.tweenTo             = copy.copy(self.currentColor)
    self.tweenChange         = copy.copy(self.currentColor)
    self.tweenTotalSteps     = 0
    self.tweenRemainingSteps = 0

  # Assumed to run self.timeScale times every second
  def loop(self):
    self.tweenColor()
    self.updateLedStrip()

  def updateLedStrip(self):
    self.ledStrip.setAll(self.currentColor)
    self.ledStrip.update()

  def toJson(self):
    return json.dumps({ 'r': self.tweenTo[0], 'g': self.tweenTo[1], 'b': self.tweenTo[2] })

  def setupTween(self, goalColor, steps):
    self.tweenFrom            = copy.copy(self.currentColor)
    self.tweenTo              = goalColor
    self.tweenChange          = map(operator.sub, self.tweenTo, self.tweenFrom)
    self.tweenTotalSteps      = steps
    self.tweenRemainingSteps  = steps

  def tweenColor(self):
    if not self.tweenRemainingSteps > 0:
      return

    thisStep = float(self.tweenTotalSteps - self.tweenRemainingSteps) + 1
    progress = thisStep / self.tweenTotalSteps

    for index in [0,1,2]:
      newValue = (self.tweenChange[index] * progress) + self.tweenFrom[index]
      self.currentColor[index] = intInRange(newValue, 0, self.tweenTo[index])

    self.tweenRemainingSteps -= 1

  def updateFromArgs(self, args):
    r = intInRange(args.get('r', [self.currentColor[0]])[0], 0, 255)
    g = intInRange(args.get('g', [self.currentColor[1]])[0], 0, 255)
    b = intInRange(args.get('b', [self.currentColor[2]])[0], 0, 255)

    seconds = intInRange(args.get('seconds', [5])[0], 1, 3600)

    self.setupTween([r,g,b], int(seconds * self.timeScale))

def intInRange(value, minValue, maxValue):
  return min(max(int(value), minValue), maxValue)
