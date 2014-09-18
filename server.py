from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from LedManager import LedManager

manager = LedManager()

colorLoop = LoopingCall(manager.loop)
colorLoop.start(1.0 / manager.timeScale)

class ColorController(Resource):
  isLeaf = True

  def setJson(self, request):
    request.setHeader("content-type", "application/json; charset=utf-8")

  def render_GET(self, request):
    self.setJson(request)
    return manager.toJson()

  def render_POST(self, request):
    self.setJson(request)
    manager.updateFromArgs(request.args)
    return manager.toJson()

if __name__ == '__main__':
  reactor.listenTCP(3000, Site(ColorController()))
  reactor.run()
