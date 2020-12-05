import requests
import time
import telegram
import os
import logging

OS_NAME = os.name
# Если не деплоим в облако, то нужна библиотека load_dotenv
if OS_NAME in ["nt", 'win32', 'cygwin', 'mac']:
    from dotenv import load_dotenv
else:
    OS_NAME = None

from MyLogger import MyLoggerFormatter, create_my_logger, create_log_message

# Сделал свой логгер, тк в будущем проект может состоять из нескольких модулей.
# Чтобы было проще логгировать работу каждого модуля необходимо создать логгер на каждый модуль.

# logger.warning("This is a Warning")


def get_user_reviews(url: str, headers: dict, params: dict = None):
    logger = logging.getLogger(f'{__name__}.get_user_reviews')
    server_response_max_time = 90
    timeout = server_response_max_time + 5
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout as e:
        error_msg = f'Произошла ошибка:\n{e}'
        create_log_message(logger_msg=logger.exception, msg=error_msg, to_telegram=True)
        return
    except requests.exceptions.ConnectionError as e:
        error_msg = f'Произошла ошибка:\n{e}'
        create_log_message(logger_msg=logger.exception, msg=error_msg)
        time.sleep(10)
        return


def get_request_long_polling(base_url: str, auth_token: str, params: dict = None):
    logger = logging.getLogger(f'{__name__}.get_request_long_polling')
    url = f'{base_url}/api/long_polling/'
    headers = {
        "Authorization": auth_token
    }
    user_reviews = get_user_reviews(url=url, headers=headers, params=params)

    if not user_reviews:
        return

    if user_reviews.get("status") == "found":
        new_attempt = user_reviews.get('new_attempts')[-1]
        lesson_title = new_attempt.get('lesson_title')
        lesson_url = f'{URL_DEVMAN}{new_attempt.get("lesson_url")}'
        is_negative = new_attempt.get('is_negative')

        positive_result = "У вас все верно, можете приступать к следующему уроку."
        negative_result = 'К сожалению, в вашей работе нашлись ошибки.'
        add_text = "Всего хорошего, "
        answer = f"""У вас проверили работу "{lesson_title}".
        {positive_result if not is_negative else negative_result}
        Работа находится по ссылке {lesson_url}
        {add_text}"""

        send_msg_to_user(chat_id=TELEGRAM_CHAT_ID, text=answer, use_name=True)

        create_log_message(logger_msg=logger.debug,
                           msg=f"Homework review was sent to chat_id={TELEGRAM_CHAT_ID}")

        return user_reviews.get("last_attempt_timestamp")

    return user_reviews.get("timestamp_to_request")


def send_msg_to_user(text: str, chat_id: int = None, use_name: bool = False, bot=None):
    if not bot:
        bot = BOT
    if not chat_id:
        chat_id = TELEGRAM_CHAT_ID
    logger = logging.getLogger(f'{__name__}.send_msg_to_user')
    try:
        chat_info = bot.get_chat(chat_id=chat_id)
        if chat_info["type"] == 'private':
            first_name = chat_info["first_name"]
            last_name = chat_info["last_name"]
            chat_name = f"{first_name} {last_name}"
        elif chat_info["type"] == 'group':
            chat_name = chat_id
        else:
            chat_name = None

        message = f'{text} {chat_name if use_name else ""}'
        bot.send_message(chat_id=chat_id, text=message)

        create_log_message(logger_msg=logger.debug,
                           msg=f"Send to chat_id: {chat_id} message: {message}")

    except telegram.error.BadRequest as e:
        create_log_message(logger_msg=logger.exception,
                           msg=f'Chat [chat_id={chat_id}] not found. If you have not send command /start to bot, '
                               f'just do it.\n Error: {e}')


if __name__ == '__main__':
    main_logger = create_my_logger(name=__name__, level=logging.INFO)

    if OS_NAME:
        load_dotenv()

    AUTHORIZATION_TOKEN_DEVMAN = os.getenv("AUTHORIZATION_TOKEN_DEVMAN")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    URL_DEVMAN = "https://dvmn.org"

    BOT = telegram.Bot(token=TELEGRAM_TOKEN)
    start_message = "Бот запущен"
    create_log_message(logger_msg=main_logger.info, msg=start_message, to_telegram=True)

    params = {
        "timestamp": None
    }

    while True:
        params["timestamp"] = get_request_long_polling(base_url=URL_DEVMAN,
                                                       auth_token=AUTHORIZATION_TOKEN_DEVMAN,
                                                       params=params)
