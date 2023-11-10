"""Представленный модуль содержит функциональность для логирования сообщений и действий в файлы.

Модуль содержит следующие функции и декораторы:

`log(func)`
Декоратор, который логирует информацию о сообщении и его отправителе. Если включен режим логирования (`LOG_MODE=True`), то создается файл лога и записывается информация о сообщении. Декоратор возвращает результат выполнения исходной функции. Принимает один аргумент `func`, который является функцией, обертку которой нужно создать.

`_get_max_size_log()`
Внутренняя функция, которая возвращает максимальный размер лог-файла в байтах, указанный в `MAX_SIZE_KB_LOG` (указан в килобайтах и конвертируется в байты).

`_clear_logs_file(file)`
Внутренняя функция, которая проверяет размер указанного файла лога и, если он превышает максимально допустимый размер, удаляет файл.

`_create_logs_if_not_exists()`
Внутренняя функция, которая создает директорию для хранения лог-файлов, если она не существует.

`_get_path_sep()`
Внутренняя функция, которая возвращает символ разделителя пути в зависимости от операционной системы.

Переменные:

`LOG_MODE`
Переменная, определяющая включен ли режим логирования. Если `True`, то логирование включено, если `False`, то логирование отключено.

`MAX_SIZE_KB_LOG`
Максимально допустимый размер лог-файла в килобайтах. Если значение равно -1, то ограничений на размер лог-файла нет.

`PATH_TO_LOG_DIR`
Путь к директории, в которой будут храниться лог-файлы.

`__all__`
Список, содержащий имена публичных объектов, которые будут импортированы при импорте модуля.

Для использования функциональности модуля необходимо импортировать декоратор `log` и использовать его для обертывания функций, которые требуется логировать.

Пример использования:

```python
from logger import log

@log
def process_message(message):
    # обработка сообщения
    pass
```

При вызове функции `process_message` информация о сообщении будет логироваться в соответствующий файл лога, если включен режим логирования.
"""


import datetime
import os

from config import LOG_MODE, MAX_SIZE_KB_LOG, PATH_TO_LOG_DIR, PRINT_DEBUG


def debug(*args, **kwargs):
    if PRINT_DEBUG:
        print('DEBUG: ', *args, **kwargs)


def log(func):
    def wrapper(message, *args, **kwargs):
        if LOG_MODE:
            path = f'{PATH_TO_LOG_DIR}{_get_path_sep()}{message.from_user.username}_{message.chat.id}.txt'
            _create_logs_if_not_exists()

            text = f'TIME: {datetime.datetime.now()}: \n\tMSG_FROM_USER: {message.text}\n'

            print(f'{message.from_user.username=} -> {message.chat.id=} -> {text}')
            with open(file=path, mode='a', encoding='utf-8') as file:
                file.write(text)

            _clear_logs_file_if_full(path)

        return func(message, *args, **kwargs)

    return wrapper


def _get_max_size_log():
    return MAX_SIZE_KB_LOG * 1024


def _clear_logs_file_if_full(file):
    stats = os.stat(file)

    if stats.st_size >= _get_max_size_log() and MAX_SIZE_KB_LOG != -1:
        os.remove(file)


def _create_logs_if_not_exists():
    if not os.path.exists(PATH_TO_LOG_DIR):
        os.mkdir(PATH_TO_LOG_DIR)


def _get_path_sep():
    if os.name == 'posix':
        return '/'
    elif os.name == 'nt':
        return '\\'


__all__ = (
    log.__name__,
)
