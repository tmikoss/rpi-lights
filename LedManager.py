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

    self.r = 0
    self.g = 0
    self.b = 0
    self.a = 0

    self.updateLedStrip()

  def updateLedStrip(self):
    self.ledStrip.setAll(map(lambda x: int(x * self.a / 100), [self.r, self.b, self.g]))
    self.ledStrip.update()

  def toJson(self):
    return json.dumps({ 'r': self.r, 'g': self.g, 'b': self.b, 'a': self.a })

  def updateFromArgs(self, args):
    self.r = intInRange(args.get('r', [self.a])[0], 0, 255)
    self.b = intInRange(args.get('b', [self.b])[0], 0, 255)
    self.g = intInRange(args.get('g', [self.g])[0], 0, 255)
    self.a = intInRange(args.get('a', [self.a])[0], 0, 100)

    self.updateLedStrip()

def intInRange(value, minValue, maxValue):
  return min(max(int(value), minValue), maxValue)
