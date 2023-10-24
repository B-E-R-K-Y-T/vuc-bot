from enum import Enum, auto, unique

from config import Message


@unique
class EditSquadUserState(Enum):
    EDIT = auto()
    FINAL = auto()


STATE = (
    EditSquadUserState.EDIT,
    EditSquadUserState.FINAL,
)

EDIT_SQUAD_USER_MSG_STATES = {
    EditSquadUserState.EDIT: Message.EditSquadUserState.EDIT,
    EditSquadUserState.FINAL: Message.EditSquadUserState.FINAL,
}
