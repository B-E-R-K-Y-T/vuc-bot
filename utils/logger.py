import datetime
import os

from config import LOG_MODE, MAX_SIZE_KB_LOG, PATH_TO_LOG_DIR


def log(func):
    def wrapper(message, *args, **kwargs):
        if LOG_MODE:
            path = f'{PATH_TO_LOG_DIR}\\{message.from_user.username}_{message.chat.id}.txt'
            _create_logs_if_not_exists()

            text = f'TIME: {datetime.datetime.now()}: \n\tMSG_FROM_USER: {message.text}\n'

            print(f'{message.from_user.username=} -> {message.chat.id=} -> {text}')
            with open(file=path, mode='a', encoding='utf-8') as file:
                file.write(text)

            _clear_logs_file(path)

        return func(message, *args, **kwargs)

    return wrapper


def _get_max_size_log():
    return MAX_SIZE_KB_LOG * 1024


def _clear_logs_file(file):
    stats = os.stat(file)

    if stats.st_size >= _get_max_size_log() and MAX_SIZE_KB_LOG != -1:
        os.remove(file)


def _create_logs_if_not_exists():
    if not os.path.exists(PATH_TO_LOG_DIR):
        os.mkdir(PATH_TO_LOG_DIR)
