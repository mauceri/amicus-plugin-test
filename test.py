import logging
from amicus_interfaces import IObserver, IObservable, IPlugin
from nio.rooms import MatrixRoom
from nio.events.room_events import RoomMessageText

logger = logging.getLogger(__name__)

class Echo(IObserver):
    def __init__(self,observable:IObservable=None):
        self.observable =observable

    async def notify(self,room:MatrixRoom, event:RoomMessageText, msg:str):
        logger.info(f"***************************** L'utilisateur {event.sender} a écrit {msg} depuis ls salon {room.name}")
        # Coco répète ce qu'on lui dit
        await self.__observable.notify(room,event,f"L'utilisateur {event.sender} a écrit {msg} depuis le salon {room.name}",None,None)

    def prefix(self):
        return "!echo"
    
class Plugin(IPlugin):
    def __init__(self,observable:IObservable):
        self.__observable = observable
        self.echo = Echo(self.__observable)
        logger.info(f"********************** Observateur créé {self.echo.prefix()}")
        
    def start(self):
        logger.info(f"********************** Inscripton de {self.echo.prefix()}")
        self.__observable.subscribe(self.echo)

    async def stop(self):
        pass