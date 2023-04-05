from enum import Enum,auto

class MessageType(Enum):
    FINISHED_ONE = auto()
    FINISHED_COMPLETELY = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class ProgressReport:
    def __init__(self,msg="") -> None:
        self.message = msg

    def setMessageType(self,messagetype: MessageType):
        self.messageType = messagetype
        return self



    @classmethod
    def fromDict(cls, tupleMessage):
        if not type(tupleMessage) is dict:
            raise TypeError(
                "Invalid Message type - expected tuple. message:" + str(tupleMessage)
            )
        key = list(tupleMessage.keys())[0]
        value = list(tupleMessage.values())[0]

        return ProgressReport(MessageType[key], value)
