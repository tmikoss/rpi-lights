from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import json

from vendor.LedStrip_WS2801 import LedStrip_WS2801

numberOfLeds = 25
currentColor = { 'r': 0, 'g': 0, 'b': 0 }

ledStrip = LedStrip_WS2801(numberOfLeds)

def setCurrentColor():
  ledStrip.setAll([currentColor['r'], currentColor['g'], currentColor['b']])
  ledStrip.update()

colorLoop = LoopingCall(setCurrentColor)
colorLoop.start(1)

class ColorController(Resource):
  isLeaf = True

  def render_GET(self, request):
    request.setHeader("content-type", "application/json; charset=utf-8")
    return json.dumps(currentColor)

  def render_POST(self, request):
    request.setHeader("content-type", "application/json; charset=utf-8")
    for key in currentColor:
      currentColor[key] = int(request.args[key][0])
    return json.dumps(currentColor)

if __name__ == '__main__':
  reactor.listenTCP(3000, Site(ColorController()))
  reactor.run()
