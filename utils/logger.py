import datetime
import os


def _create_logs_if_not_exists():
    path = '.\\logs'
    if not os.path.exists(path):
        os.mkdir(path)


def log(flag=True):
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            if flag:
                _create_logs_if_not_exists()

                text = f'TIME: {datetime.datetime.now()}: \n\tMSG_FROM_USER: {message.text}\n'

                print(f'{message.from_user.username=} -> {message.chat.id=} -> {text}')
                with open(file=f'.\\logs\\{message.from_user.username}_{message.chat.id}.txt', mode='a') as file:
                    file.write(text)

            return func(message, *args, **kwargs)

        return wrapper

    return decorator
