Notification bot for Devman.org
======

Бот для отправки уведомлений о результатах проверки домашних заданий для сайта devman.org.<br>
Уведомления приходят в мессенджер Telegram.

#### Бот работает с версиями Python 3.6+ <br>С версиями ниже бот не работает!!!

## Настройка для использования на личном ПК
1. Скачайте проект с гитхаба
2. Перейдите в папку с ботом с помощью консоли и команды `cd <путь до проекта devman_bots_development>`<br>
3. Установить зависимости из файла `requirements.txt`<br>
   Библиотеки к установке: `requests`, `python-telegram-bot`. Если вы не используете облачные сервисы для деплоя, то добавьте в файл `requirements.txt` строку `dotenv`<br>
   
   Возможные команды для установки:<br>
   `pip3 install -r requirements.txt`<br>
   `python -m pip install -r requirements.txt`<br>
   `python3.6 -m pip install -r requirements.txt`
4. Создайте файл .env
5. Запишите в файл .env переменные:
    `AUTHORIZATION_TOKEN_DEVMAN=ваш_токен_девмана`<br>
    `TELEGRAM_TOKEN=ваш_токен_телеграм_бота`<br>
    `TELEGRAM_CHAT_ID=ваш_телеграм_айди`<br>
6. Запустите бота<br>
   Возможные команды для запуска(из консоли, из папки с ботом):<br>
   `python3 main.py`<br>
   `python main.py`<br>
   `python3.6 main.py`<br>
   
## Настройка для деплоя в облако Heroku
Если не знаем что такое Heroku - гуглим мануал или используем настройку бота из предыдущего туториала
1. Создайте `app` на Heroku 
2. Перейдите в созданный `app` и выберите GitHub в качестве `Deployment method`
3. Укажите адрес до **вашего!!!** проекта на гитхабе
4. Выберите ветку main в разделе `Manual deploy` и нажмите на кнопку `Deploy Branch`
5. Зайдите в раздел `Settings`
6. Запишите в раздел `Config Vars` переменные `KEY` и `VALUE`:
    `AUTHORIZATION_TOKEN_DEVMAN=ваш_токен_девмана`<br>
    `TELEGRAM_TOKEN=ваш_токен_телеграм_бота`<br>
    `TELEGRAM_CHAT_ID=ваш_телеграм_айди`<br>
7. Перейдите в раздел `Resources` и включите бота<br> 
   Логи можно посмотреть в `More` -> `View logs`
  