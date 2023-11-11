from utils.exceptions import MaxEventIndexException
from utils.singleton import singleton

_MAX_COUNT_INDEX = 100


class EvenIndexIterator:
    def __iter__(self):
        return EventIndexGenerator()


@singleton
class EventIndexGenerator:
    def __init__(self):
        self.event_index = 0

    def __next__(self):
        self.event_index += 1

        # Это сделано, чтобы не попасть в бесконечный цикл и при этом явно сообщить, что итерация закончена.
        if self.event_index > _MAX_COUNT_INDEX:
            raise MaxEventIndexException(f'Достигнуто максимальное кол-во событий в боте!'
                                         f'\n\n{self.event_index} > {_MAX_COUNT_INDEX}'
                                         f'\n\nЕсли Вы хотите это изменить, то поменяйте значение константы:'
                                         f'_MAX_COUNT_INDEX')

        return self.event_index


@singleton
class AutoEventIndexGenerator:
    def __init__(self):
        self.event_generator = iter(EvenIndexIterator())

    def __call__(self):
        return next(self.event_generator)


def auto_event_id():
    return f'event_{AutoEventIndexGenerator()()}'


__all__ = (
    EvenIndexIterator.__name__,
    auto_event_id.__name__,
)


if __name__ == '__main__':
    e = EvenIndexIterator()

    print(auto_event_id())
    print(auto_event_id())
    print(auto_event_id())

    print('-' * 100)

    for i in e:
        print(i)
