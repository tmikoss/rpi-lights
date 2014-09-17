import platform
import json

if platform.system() == 'Darwin':
  from MockLedStrip import LedStrip_WS2801
else:
  from vendor.LedStrip_WS2801 import LedStrip_WS2801

class LedManager:
  def __init__(self):
    self.ledCount = 25
    self.ledStrip = LedStrip_WS2801(self.ledCount)

    self.currentR = 0.0
    self.currentG = 0.0
    self.currentB = 0.0

  def loop(self):
    self.ledStrip.setAll([int(self.currentR), int(self.currentG), int(self.currentB)])
    self.ledStrip.update()

  def toJson(self):
    return json.dumps({ 'r': int(self.currentR), 'g': int(self.currentG), 'b': int(self.currentB)})

  def updateFromArgs(self, args):
    self.currentR = float(args.get('r', [self.currentR])[0])
    self.currentG = float(args.get('g', [self.currentG])[0])
    self.currentB = float(args.get('b', [self.currentB])[0])
