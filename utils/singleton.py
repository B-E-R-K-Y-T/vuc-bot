def singleton(class_):
    __instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in __instances:
            __instances[class_] = class_(*args, **kwargs)
        return __instances[class_]

    return getinstance
