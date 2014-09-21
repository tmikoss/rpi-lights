class LedStrip_WS2801(object):
  def __init__(self, numberOfLeds):
    self.numberOfLeds = numberOfLeds
    self.colorArray = [0,0,0]

    print 'Initialized {0} LED strip'.format(self.numberOfLeds)

  def setAll(self, colorArray):
    self.colorArray = colorArray;

  def update(self):
    print self.colorArray;
