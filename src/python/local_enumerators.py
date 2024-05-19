from enum import Enum

class CallState(Enum):
    ANSWERED = 1
    HANGUP = 2
    BUSY = 3