# Errata note: when TNPE 2ed was first printed, Twisted 12.0.0 was the latest
# version of Twisted. Since then, passing bare strings to the errback method
# was deprecated in Twisted 12.3.0. A failure or Exception must now be
# passed instead.

from twisted.internet import reactor, defer


class HeadlineRetriever(object):

    def processHeadline(self, headline):
        if len(headline) > 50:
            self.d.errback(
                ValueError("The headline ``%s'' is too long!" % (headline,)))
        else:
            self.d.callback(headline)

    def _toHTML(self, result):
        return "<h1>%s</h1>" % (result,)

    def getHeadline(self, input):
        self.d = defer.Deferred()
        reactor.callLater(1, self.processHeadline, input)
        self.d.addCallback(self._toHTML)
        return self.d


def printData(result):
    print result
    reactor.stop()


def printError(failure):
    print failure
    reactor.stop()

h = HeadlineRetriever()
d = h.getHeadline("Breaking News: Twisted Takes us to the Moon!")
d.addCallbacks(printData, printError)

reactor.run()
