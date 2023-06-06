# ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
В переменную окружения можно записать данные, а потом вызвать ее. Например, в ней удобно хранить токены, настройки.

Вспомним наш код из 3 урока:
```Dockerfile
FROM ubuntu:20.04

RUN apt-get update && apt-get install -y nano wget curl git

WORKDIR /home/igor

COPY random_file.txt random_file.txt

# Изменим интерфейс терминала в контейнере
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t robbyrussell \
    -p https://github.com/zsh-users/zsh-autosuggestions

ENV ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#dedede,bg=#9c9c9c,bold,underline"

# Запустим оболочку
ENTRYPOINT [ "zsh" ]

# Добавим скрипт приветсвтвия и запустим его
RUN touch hello.sh && echo "echo 'Hello from container'" > hello.sh
CMD [ "hello.sh" ]
```

Здесть есть мы создавали переменную окружения ```ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE```. И в самом докерфайле нельзя хранить токены и пароли!!! 
Секретную переменную окружения можно прокинуть при запуске контейнера:
```bash
docker run -it --rm -e ENV_VAR=42 ubuntu
echo $ENV_VAR
```
```echo $ENV_VAR``` - Вызывает переменную ENV_VAR.

Переменную заданную в Dockerfile можно переопределить при запуске контейнера!
## ПРАКТИКА
Исправим телеграм-бота из урока 4. Прокинем в него токен.

В файле *tg_bot.py* сделаем замену:
```python
with open ('TOKEN.txt', 'r') as file:
    APP_TOKEN_FROM_FILE = file.read()
# ============ !!! Секретный токен !!! ===============
APP_TOKEN = APP_TOKEN_FROM_FILE
# ====================================================

# На токен из переменной окружения
APP_TOKEN = os.environ.get("APP_TOKEN")
```

Теперь нужно запускать контейнер с указанием переменной APP_TOKEN

# ЛОГИ
Рассмотрим 2 потока вывода в Python:
```Python
from random import randint
from sys import stderr
from time import sleep


def main():
    while True:
        value = randint(-2,2)

        try:
            sleep(value)
        except ValueError as e:
            print(e, file=stderr)  # Поток вывод ошибок 
            continue

        print(f"Random value ={value}")  # Стандартный поток вывода stdout
if __name__ == "__main__":
    main()
```

Запустим скрипт c выводом логов в файл:
```bash
python3 logs_example.py > stdout.txt 2> stderr.txt
cat stdout.txt
# Увидим стандартный поток вывода
cat stderr.txt
# Увидим поток вывода ошибок
```

Как с этим работать в контейнере?
Рассмотрим 3 варианта программы:
1. logs_console.py - который приведен выше
2. logs_file.py - значения будем записывать в файлик logs.txt
3. logs_lib - аналог первого (в консоль), но через библиотеку logging

Посмотрим сборку:
```Dockerfile
FROM python:3.8

WORKDIR /logs

COPY ./logs_console.py ./console

COPY ./logs_lib.py ./lib

COPY ./logs_file.py ./file

ENTRYPOINT ["python3", "-u"]
```

## 1. Реализация через файл
Соберем образ и поднимем контейнеры:
```bash
docker build -t logs_ex:1 .
docker run --name file_ex logs_ex:1 file
docker exec -it file_ex bash
# Увидим список файлов
ls
# Посмотрим лог файл
cat logs.txt
```
Чтобы получить логи, надо сделать маунт файл, чтобы данные сохранялись на компьютер.

## 2. Реализация через потоки вывода - самый простой вариант
Интересный вариант, когда логи пишутся в OUTPUT(консоль), что делать с ними? У Docker есть API для взаимодействия с ними.
```bash
docker run --name console_ex logs_ex:1 console
docker logs -f -t console_ex
```
Получим логи в консоли через ```docker logs``` с флагом ```-f``` (чтобы не выходить сразу) и флагом ```-t```, чтобы он указывал время.
Это самый простой вариант логгирования, так как не нужно маунтить файл для логирования.
Также существует команда:
```bash
docker inspect --format "{{.LogPath}}" console_ex
```
которая выводит расположение логов на хосте.

## 3. Реализация через библиотеку
```bash
docker run --name lib_ex logs_ex:1 lib
```
Остановим контейнер и выведем логи, но выведем 5 первых строк:
```bash
docker logs lib_ex | head -n 5
```
Не сработало - вывел все логи, тогда выведем из логов сообщения, содержащие ERROR:
```bash
docker logs lib_ex | grep ERROR
```
Опять вывел все логи.

А теперь посмотрим логи с head для контейнера console_ex:
```bash
docker logs lib_ex | head -n 5
```
Аналогично, выходят все логи.
Команды grep и head при работе ловят стандартный поток вывода. А библиотека записывает в стандартынй поток ошибок, а head и grep не принимают стандартный поток ошибок.
Как здесь быть? Самый простой способ - перенаправить стандартный поток вывода на стандартный поток ошибок:
Указываем стандартный поток ошибок ```2>```, а дальше указываем стандартный поток вывода ```&1```
```bash
docker logs lib 2>&1 | grep ERROR
```
Теперь все работает.

# ПОРТЫ
Веб-приложения используют порты, для обращения к ним. Если запустить контейнер с приложением, использующий порт, но не прокинем его при запуске, то мы не сможем достучаться до вебприложения вне контейнера (с хоста или другого устройства). Для того, чтобы прокинуть контейнер используется флаг ```-p``` при запуске:
```bash
docker run -it --rm -p 80:80 web-app 
```
Первый порт на хосте, второй - в контейнере.

При сборке образов нужно указывать порты, которые нужны для работы приложения и делается это так:
```Dockerfile
EXPOSE 22
EXPOSE 80
```
Но стоит помнить, что это больше как подсказка. Прокидывать порты при запуске все равно нужно! Также можно прокинуть все порты из EXPOSE при помощи флага ```-P```.
Нельзя запускать контейнеры на одном и том же порту! На хосте можно указать другой порт для решения проблемы

Можно прокинуть несколько портов, задав опцию ```-p``` несколько раз:
```bash
docker run -p 80:80 -p 81:80 -p 82:80 nginx
```

# РАЗВОРАЧИВАЕМ ЛОКАЛЬНО БАЗЫ ДАННЫХ
Поднимаем БД:
```bash
docker run --rm -d -p 8123:8123 -p 9000:9000 --name ch_db yandex/clickhouse-server
```
Попробуем обратиться через Visual Studio Code, установив плагин SQLTools и драйвер Snowflake Driver for SQLTools:
Не вышло, разобраться. Можно через python: см. ddl.py - пример.

Подключимся через tabix:
```bash
docker pull spoonest/clickhouse-tabix-web-client
docker run -d -p 8080:80 spoonest/clickhouse-tabix-web-client
```
Перейдем с хоста по адресу localhost:8080
ip: 127.0.0.1:8123
login: default
password: 

Создадим БД: 
```SQL
CREATE DATABASE todo_list;
```

Создадим таблицу:
```SQL
CREATE TABLE todo_list;
```

Добавим в нее таблицу todo_list (id, text, status). Добавим элемент таблицы и выведем его значение. 

## Теперь поработаем с superset и postgres:

### 1. Поднимем Postgres
```bash
docker run -d --rm -e POSTGRES_PASSWORD=admin -e POSTGRES_USER=admin -e POSTGRES_DB=todo_db -p 5432:5432 postgres:14
```
Если не указать название БД - то дефолтное будет: template1
### 2. Поднимем superset
```bash
docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=My_Super_Secret_Password" --name superset apache/superset
```
Настроим аккаунт админа:
```bash
docker exec -it superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin
```

Migrate local DB to latest
```bash
docker exec -it superset superset db upgrade
```

Setup roles
```bash
docker exec -it superset superset init
```

Далее, нажем плюсик - Data - Connect database - Postgresql.
HOST: 127.0.0.1 - не выйдет (или 172.17.0.1 или 127.0.0.2 и т.д.)
PORT: 5432
DATABASE NAME: todo_db
USERNAME: admin
PASSWORD: admin

Обязательно отмечаем галочками следующие пункты:
- Expose database in SQL Lab
- Allow CREATE TABLE AS
- Allow CREATE VIEW AS
- Allow DML

Далее перейдем в SQL Lab. Выберем SCHEMA Public. Создадим таблицу:
```SQL
CREATE TABLE todo_list (
  id TEXT NOT NULL,
  text TEXT NOT NULL,
  status TEXT NOT NULL
);
```
Добавим данные, выберем таблицу и выведем данные:
```SQL
INSERT INTO todo_list (id, text, status) VALUES ('1', 'Купить масло', 'active');
SELECT * FROM todo_list
```

## Телеграм бот и база данных
Изменим бота так, чтобы он сохранял данные не в файлик, а в БД яндекс клик хаус.

Через ddl.py (DDL - Data Definition Language) создаем БД и таблицу в ней. А в tg_bot.py уже работаем с этой таблицей (DML). Читаем и записываем.

Если бота поднимаем локально, то проблем нет. Теперь завернем его в контейнер. Теперь бот не работает, не может подключиться к БД.

# Некоторые задания:
Прокинуть все переменные окружения в контейнер:
--env-file .env

Хоть логов у нас всего 12 (7 - stdout и 5 - stderr), мы воспользовались дозаписью в файл. То есть вначале (echo '' > logs.log) мы "обнулили" файл и в первую строку положли '' (то есть пустую строку). После этого дозаписывали в конец логи из stdout и stderr.

```bash
echo '' > logs.log && docker logs logs_task >> logs.log 2>> logs.log.
```

Таким образом, используя операторы ```>```, ```>>```, ```2>``` и ```2>>``` мы можем сохранить все наши логи в файлики, а затем смотреть на них (например обработать их при помощи кода).

Еще раз подытожим:

- ```>``` — запись stdout в файл
- ```>>``` — дозапись stdout в файл
- ```2>``` — запись stderr в файл
- ```2>>``` — дозапись stderr в файл

Чтобы узнать, какой порт слушает веб приложение (если это не указано в EXPOSE), то нужно перейти в контейнер и выполнить в нем команду:
```bash
lsof
```
И найти порт, у которого написано LISTEN.