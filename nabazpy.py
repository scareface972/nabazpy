from twisted.web.client import getPage
from twisted.internet.defer import Deferred

from urllib import urlencode

class NabazPy(object):
    """
    Exemple utilisation:
    
    #-*- encoding:iso8859-1 -*-

    from twisted.internet import reactor
    from nabazpy import NabazPy

    SN = "0019DB9DB819"
    TOKEN = "1236642458"

    def sendMessageCallback(result):
        print result

    if __name__ == "__main__":

        lapin = NabazPy(SN, TOKEN)
        lapin.sendMessage("Tu es beau").addCallback(sendMessageCallback)
        lapin.choregraphy("10,0,motor,1,20,0,0,10,0,motor,1,10,0,0").addCallback(sendMessageCallback)
        lapin.listenStreams(["http://www.tv-radio.com/station/france_inter_mp3/france_inter_mp3-128k.m3u"]).addCallback(sendMessageCallback)

        reactor.run()
    """

    def __init__(self, serialnumber, tocken, urlapi="http://api.nabaztag.com/vl/FR/api.jsp"):
        self.__serialnumber = serialnumber
        self.__tocken = tocken
        self.__urlapi = urlapi

    def sendMessage(self, message, voice="FR-Anastasie"):
        """
        @param message: send message to nabaztag
        @type message: str
        @return : Deferred
        """

        d = Deferred()

        def processedApiResult(result):
            d.callback(result)
            return d

        def processedApiFailed(faillure):
            d.errback(faillure)
            return d

        postdata = {"sn":self.__serialnumber,
                    "token":self.__tocken,
                    "tts":message,
                    "voice":voice}

        getPage(self.__urlapi,
                method="POST",
                postdata=urlencode(postdata),
                headers={'Content-Type':'application/x-www-form-urlencoded;\
                          charset=3Dutf-8'}).addCallback(processedApiResult).addErrback(processedApiFailed)

        return d

    def choregraphy(self, choregraphy):
        """
        @param choregraphy: describe choregra
        @type message: str
        @return : Deferred

        LED commands

        It is a series of values separated by commas.
        1. First value : action time (' l'heure ')
            ("0" if it is the first command).
        2. Second value : 'led' , which gives a color to the LED.
        3. Third value : To define which LED you want to illuminate.
            0 : bottom LED
            1 : rabbit's left LED
            2 : middle LED
            3 : rabbit's right LED
            4 : high LED
        4. Fourth, Fifth, Sixth value : the color in RGB.
            Value from 0 to 255

        Ears commands

        This is a series of values separated by commas.
        The command is as follows :
        1. First value : Action time (l'heure)
            "0" if it is the first command.
        2. Second value : 'motor', to move an ear
        3. Third value : Ears command
            1 to command left ear
            0 to command right ear
        4. Fourth value : Angle of ear
            Possible value from 0 to 180
        5. Fifth value : Unused, set at "0"
        6. Sixth value : Rotation of the ears directions
            1 : high->back->low->front->high...
            0 : high->front->low->back->high...

        Exemple :

        0,motor,1,20,0,0

        0,led,2,0,238,0,2,led,1,250,0,0,3,led,2,0,0,0

        10,0,motor,1,20,0,0,0,led,2,0,238,0,2,led,1,250,0,0,3,led,2,0,0,0

        """

        d = Deferred()

        def processedApiResult(result):
            d.callback(result)
            return d

        def processedApiFailed(faillure):
            d.errback(faillure)
            return d

        postdata = {"sn":self.__serialnumber,
                    "token":self.__tocken,
                    "chor":choregraphy}

        getPage(self.__urlapi,
                method="POST",
                postdata=urlencode(postdata),
                headers={'Content-Type':'application/x-www-form-urlencoded;\
                          charset=3Dutf-8'}).addCallback(processedApiResult).addErrback(processedApiFailed)

        return d

    def listenStreams(self, urlsStream):
        """
        @param urlsStream: Definit les url de stream a ecouter
        @type urlsStream: tableau d'url
        @return : Deferred
        Exemple:
            lstream = ["http://my.server.org/music.mp3", "http://m.server.org/music2.mp3"]
            instanceNabaz.listenStreams(lstreams).addCallback(lambda x: print x)
        API Nabastag : ?token=xxx&sn=xxx&urlList=http://my.server.org/music.mp3|http://m.server.org/music2.mp3
        """

        paramUrlsStream = '|'.join(urlsStream)
        print paramUrlsStream

        d = Deferred()

        def processedApiResult(result):
            d.callback(result)
            return d

        def processedApiFailed(faillure):
            d.errback(faillure)
            return d

        postdata = {"sn":self.__serialnumber,
                    "token":self.__tocken,
                    "urlList":paramUrlsStream}

        getPage(self.__urlapi,
                method="POST",
                postdata=urlencode(postdata),
                headers={'Content-Type':'application/x-www-form-urlencoded;\
                          charset=utf-8'}).addCallback(processedApiResult).addErrback(processedApiFailed)

        return d
