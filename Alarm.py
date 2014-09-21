from twisted.internet import reactor
from crontab import CronTab

class Alarm(object):
  def __init__(self, cronString, ledManager, seconds=60, goalAlpha=100):
    self.ledManager = ledManager
    self.cron       = CronTab(cronString)

    self.tickDelta  = 0.5
    self.ticks      = seconds / self.tickDelta
    self.goalAlpha  = goalAlpha

    self.nextRun    = reactor.callLater(self.cron.next(), self.run)

  def run(self):
    self.nextRun = reactor.callLater(self.cron.next(), self.run)
    self.scheduleIncrements()

  def cancel(self):
    if self.nextRun:
      self.nextRun.cancel()

    if self.nextIncrement:
      self.nextIncrement.cancel()

  def scheduleIncrements(self):
    self.currentAlpha = float(self.ledManager.a)

    self.incrementBy = float(self.goalAlpha - self.currentAlpha) / self.ticks

    self.nextIncrement = reactor.callLater(self.tickDelta, self.increment)

  def increment(self):
    self.currentAlpha += self.incrementBy

    self.ledManager.a = self.currentAlpha

    if self.currentAlpha < self.goalAlpha:
      self.nextIncrement = reactor.callLater(self.tickDelta, self.increment)
