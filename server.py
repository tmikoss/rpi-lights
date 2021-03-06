from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor

from LedManager import LedManager

manager = LedManager()

class ColorController(Resource):
  isLeaf = True

  def setJson(self, request):
    request.setHeader("content-type", "application/json; charset=utf-8")

  def render_GET(self, request):
    self.setJson(request)
    return manager.colorJson()

  def render_POST(self, request):
    self.setJson(request)
    for key in ['r', 'g', 'b', 'a']:
      setattr(manager, key, request.args.get(key, [getattr(manager, key)])[0])
    return manager.colorJson()

if __name__ == '__main__':
  root = File('./public')
  root.putChild('api', ColorController())
  reactor.listenTCP(3000, Site(root))
  reactor.run()
