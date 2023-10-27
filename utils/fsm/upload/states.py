from enum import Enum, auto, unique

from config import Message


@unique
class UploadState(Enum):
    UPLOAD_FILE = auto()
    FINAL = auto()


STATE = (
    UploadState.UPLOAD_FILE,
    UploadState.FINAL,
)

UPLOAD_PLATOON_MSG_STATES = {
    UploadState.UPLOAD_FILE: Message.UploadPlatoon.UPLOAD,
    UploadState.FINAL: Message.UploadPlatoon.FINAL,
}
