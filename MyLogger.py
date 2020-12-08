import logging
import datetime as dt
from __main__ import send_msg_to_user


class MyLoggerFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        converted_time = self.converter(record.created)
        if datefmt:
            time_with_sec = converted_time.strftime(datefmt)
        else:
            time_no_sec = converted_time.strftime("%Y-%m-%d %H:%M:%S")
            time_with_sec = "%s.%03d" % (time_no_sec, record.msecs)
        return time_with_sec


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, msg):
        pass


def create_my_logger(name, level):
    """Создаем и настраиваем кастомный логгер для каждого модуля"""

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(level)

    console = logging.StreamHandler()
    custom_logger.addHandler(console)

    formatter = MyLoggerFormatter(fmt="%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S.%f')
    console.setFormatter(formatter)

    custom_logger.debug(f" {__name__}.create_my_logger - Create logger for {name}")
    return custom_logger


def create_log_message(logger_msg, msg: str, to_telegram=False, func=None):
    """Логгируем действие и если необходимо, отправляем уведомление в телеграм вместе с полученным сообщением"""
    if func:
        msg = f' {func} - {msg} '
    logger_msg(msg)
    if to_telegram:
        send_msg_to_user(text=msg)
        module_MyLogger_logger.debug(f" {__name__}.create_log_message - Send notification to telegram")


module_MyLogger_logger = create_my_logger(name=__name__, level=logging.INFO)



