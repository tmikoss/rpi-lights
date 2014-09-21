import platform
import json
import copy
import operator
from twisted.internet import reactor

from Alarm import Alarm

if platform.system() == 'Darwin':
  from MockLedStrip import LedStrip_WS2801
else:
  from vendor.LedStrip_WS2801 import LedStrip_WS2801

class LedManager(object):
  def __init__(self):
    self.ledCount = 25
    self.ledStrip = LedStrip_WS2801(self.ledCount)

    self.nextTurnOff = None
    self.idleTimeoutSeconds = 60*60

    self._r      = 255
    self._g      = 255
    self._b      = 255
    self._a      = 0
    self._alarms = []

    self.alarms  = [
      "30 6 * * 1,2,3,4,5",
      "30 8 * * 6,7"
    ]

    self.updateLedStrip()

  @property
  def r(self):
    return self._r

  @r.setter
  def r(self, value):
    self._r = intInRange(value, 0 , 255)
    self.updateLedStrip()

  @property
  def g(self):
    return self._g

  @g.setter
  def g(self, value):
    self._g = intInRange(value, 0 , 255)
    self.updateLedStrip()

  @property
  def b(self):
    return self._b

  @b.setter
  def b(self, value):
    self._b = intInRange(value, 0 , 255)
    self.updateLedStrip()

  @property
  def a(self):
    return self._a

  @a.setter
  def a(self, value):
    self._a = intInRange(value, 0 , 100)
    self.updateLedStrip()

  @property
  def alarms(self):
    return map(str, self._alarms)

  @alarms.setter
  def alarms(self, value):
    for alarm in self._alarms:
      alarm.cancel()
      self._alarms.remove(alarm)

    for alarmString in value:
      self._alarms.append(Alarm(alarmString, self, seconds=30*60))

  def updateLedStrip(self):
    if self.nextTurnOff and self.nextTurnOff.active():
      self.nextTurnOff.cancel()

    self.ledStrip.setAll(map(lambda x: int(x * self.a / 100), [self.r, self.b, self.g]))
    self.ledStrip.update()

    if self.a > 0:
      self.nextTurnOff = reactor.callLater(self.idleTimeoutSeconds, self.turnOff)

  def colorJson(self):
    return json.dumps({ 'r': self.r, 'g': self.g, 'b': self.b, 'a': self.a })

  def turnOff(self):
    self.a = 0

def intInRange(value, minValue, maxValue):
  return min(max(int(value), minValue), maxValue)
