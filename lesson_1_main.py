import requests
import time
import telegram
import os
from dotenv import load_dotenv


def get_user_reviews(url: str, headers: dict, params: dict = None):
    server_response_max_time = 90
    timeout = server_response_max_time + 5
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ReadTimeout:
        return
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        return


def get_request_long_polling(base_url: str, auth_token: str, params: dict = None):
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

        return user_reviews.get("last_attempt_timestamp")

    return user_reviews.get("timestamp_to_request")


def send_msg_to_user(chat_id: int, text: str, use_name: bool = False):
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
    except telegram.error.BadRequest as e:
        print(f'Chat [chat_id={chat_id}] not found. '
              f'If you have not send command /start to bot, just do it.\n Error: {e}')


if __name__ == '__main__':
    load_dotenv()

    AUTHORIZATION_TOKEN_DEVMAN = os.getenv("AUTHORIZATION_TOKEN_DEVMAN")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    URL_DEVMAN = "https://dvmn.org"

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    params = {
        "timestamp": None
    }

    while True:
        params["timestamp"] = get_request_long_polling(base_url=URL_DEVMAN, auth_token=AUTHORIZATION_TOKEN_DEVMAN, params=params)
