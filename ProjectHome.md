Simple proxy API for control your Nabaztag|Nabaztag:tag with Python.

Exemple :

---


```
#-*- encoding:iso8859-1 -*-

from twisted.internet import reactor
from nabazpy import NabazPy

SN = "XXXXXX"
TOKEN = "XXXXXX"

def sendMessageCallback(result):
    print result

if __name__ == "__main__":

    lapin = NabazPy(SN, TOKEN)
    lapin.sendMessage("Tu es beau").addCallback(sendMessageCallback)
    lapin.choregraphy("10,0,motor,1,20,0,0,10,0,motor,1,10,0,0").addCallback(sendMessageCallback)
    lapin.listenStreams(["http://www.tv-radio.com/station/france_inter_mp3/france_inter_mp3-128k.m3u"]).addCallback(sendMessageCallback)

    reactor.run()
```