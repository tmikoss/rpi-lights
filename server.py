from twisted.web import server, resource
from twisted.internet import reactor, endpoints
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
colorLoop.start(0.5)

class ColorController(resource.Resource):
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
  endpoints.serverFromString(reactor, "tcp:3000").listen(server.Site(ColorController()))
  reactor.run()
