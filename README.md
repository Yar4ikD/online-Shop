# Интернет-магазин MEGANO
Владелец торгового центра во время COVID-карантина решил перевести своих арендодателей в онлайн. Сделать это он намерен с помощью создания платформы, на которой продавцы смогут разместить информацию о себе и своём товаре. Онлайновый торговый центр или, другими словами, интернет-магазин, являющийся агрегатором товаров различных продавцов.

## Как установить
Для работы сервиса требуются:
- Python версии не ниже 3.10.
- установленное ПО для контейнеризации - [Docker](https://docs.docker.com/engine/install/).
- Инструмент [poetry](https://python-poetry.org/) для управления зависимостями и сборкой пакетов в Python.

Настройка переменных окружения
1. Скопируйте файл .env.dist в .env
2. Заполните .env файл. Пример:
```yaml
DATABASE_URL = postgresql://skillbox:secret@127.0.0.1:5434/market
REDIS_URL = redis://127.0.0.1:6379/0
```

Запуск СУБД Postgresql
```shell
docker run --name skillbox-db -e POSTGRES_USER=skillbox -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=market -p 5434:5432 -d postgres
```
Запуск брокера сообщений REDIS
```shell
docker run --name redis-db -d redis
```
Установка и активация виртуального окружения
```shell
poetry install  ; установка пакетов
poetry shell  ; активация виртуального окружения
pre-commit install  ; установка pre-commit для проверки форматирования кода, см. .pre-commit-config.yaml
```
### Как удалить контейнеры
СУБД Postgres
```
docker rm -f -v skillbox-db
```

Брокер сообщений REDIS
```
docker rm -f -v redis-db
```

## Проверка форматирования кода
Проверка кода выполняется из корневой папки репозитория.
* Анализатор кода flake8
```shell
flake8 market
```
* Линтер pylint
```shell
pylint --rcfile=.pylintrc market/*
```
* Линтер black
```shell
black market
```

## Как запустить web-сервер
Запуск сервера производится в активированном локальном окружение из папки `market/`
```shell
python manage.py runserver 0.0.0.0:8000
```
## Добавление пользователей в модели User и Profile
После создания проекта выполнете миграции и запустите СУБД.
Запуск команды производится из папки `market/`
```shell
python manage.py add_new_users
```

## Запуск файла импорта в рамках задачи в другом процессе
Чтобы импорт товаров из файла запускался в другом процессе и не нагружал основной процесс,
нужно запустить celery в дополнительных терминалах

1 терминал
```shell
celery -A config worker -l info
```
2 терминал
```shell
celery -A config beat -l info
```
Если нужно какой-либо файл отправить без очереди, то нужно воспользоваться командой.
Можно указать только email, только название файла для импорта, либо и то и другое
```shell
python manage.py import_yaml --file filename.yaml --email example@mail.com
```

# Цели проекта

Код написан в учебных целях — это курс по Джанго на сайте [Skillbox](https://go.skillbox.ru/education/course/django-framework).
