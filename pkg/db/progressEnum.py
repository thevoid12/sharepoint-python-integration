import enum


class ProgressEnum(enum.Enum):
    DOWNLOADED = "DOWNLOADED"
    READYTOPARSE = "READYTOPARSE"
    PARSED = "PARSED"
