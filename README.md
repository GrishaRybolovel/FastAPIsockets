# FastAPIsockets

## Чтобы запустить проект, нужно:

### 1. Склонировать репозиторий к себе на компьютер
### 2. Далее можно запустить проект через Docker:
* docker-compose up

### Или же через виртуальное окружение python:
* 1. python3 -m venv env
* 2. source env/bin/activate
* 3. pip install -r requirements.txt
* 4. python3 main.py
* 5. Перейти в любом удобном для вас браузере по адресу http://0.0.0.0:8000

## Что сделано в данном проекте?
* Пользователь может задавать себе имя 
![имя](https://github.com/GrishaRybolovel/FastAPIsockets/blob/master/name.png)
* Вот так выглядит процесс общения между пользователями. Их может быть сколь угодное количество
![пользователи](https://github.com/GrishaRybolovel/FastAPIsockets/blob/master/users.png)

* Также при обновлении страницы, имя пользователя сохраняется
* Сообщения приходят real-time с помощью вебсокетов
* Также, как вы можете заметить, пользователь видит список онлайн участников чата
