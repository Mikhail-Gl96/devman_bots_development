import logging
import datetime as dt


class MyLoggerFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


def create_my_logger(name, level):
    """Создаем и настраиваем кастомный логгер для каждого модуля"""

    custom_logger = logging.getLogger(name)
    custom_logger.setLevel(level)

    console = logging.StreamHandler()
    custom_logger.addHandler(console)

    formatter = MyLoggerFormatter(fmt="%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S.%f')
    console.setFormatter(formatter)

    module_MyLogger_logger.debug(f" .create_my_logger - Create logger for {name}")
    return custom_logger


def create_log_message(logger_msg, msg: str, to_telegram=False, func=None):
    """Логгируем действие и если необходимо, отправляем уведомление в телеграм вместе с полученным сообщением"""
    if func:
        msg = f' .{func} - {msg} '
    try:
        # Импорт глобальных переменных из главного модуля, чтобы сработа функция send_msg_to_user
        # Импорт в начале файла сделать не получится, тк переменные еще не существуют в главном модуле
        from __main__ import send_msg_to_user, BOT, TELEGRAM_CHAT_ID
        module_MyLogger_logger.debug(f" .create_log_message - Import send_msg_to_user, BOT, TELEGRAM_CHAT_ID is True")
    except Exception as e:
        module_MyLogger_logger.warning(e)
    logger_msg(msg)
    if to_telegram:
        send_msg_to_user(text=msg)
        module_MyLogger_logger.debug(f" .create_log_message - Send notification to telegram")


module_MyLogger_logger = create_my_logger(name=__name__, level=logging.INFO)


