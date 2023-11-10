from config import Role, MenuButtons

MENU = {
    Role.ADMIN: {
        ...: ...,
    },

    Role.COMMANDER_PLATOON: {
        ...: ...,
    },

    Role.COMMANDER_SQUAD: {
        MenuButtons.SQUAD: {
            MenuButtons.ATTENDANCE: ...,
            MenuButtons.BACK: ...,
        },
    },

    Role.STUDENT: {
        MenuButtons.EVALUATION: {
            MenuButtons.EDIT: ...,
            MenuButtons.BACK: ...,
        },
        MenuButtons.ATTENDANCE: {
            MenuButtons.EDIT: ...,
            MenuButtons.BACK: ...,
        },
        MenuButtons.PERSONAL_DATA: {
            MenuButtons.EDIT: print,
            MenuButtons.BACK: ...,
        },
    },
}
