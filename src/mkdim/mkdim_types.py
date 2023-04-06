from enum import Enum,auto

class SourceType(Enum):
    INVALID = auto()
    DEFAULT_DIM = auto()
    DEFAULT_DAZ = auto()
    CONTAINTS_CONTENT_WITH_MANIFEST = auto()
    CONTAINTS_CONTENT_NO_MANIFEST = auto()
    CONTAINS_CONTENT=auto()
