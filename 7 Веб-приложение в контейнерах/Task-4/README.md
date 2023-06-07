Настало время поднять веб-сайт!

Итак, у вас будет 3 образа — бекенд, фронтенд и база данных.

**База данных** (постгрес):

- Нужно взять образ postgres
- При поднятии подключить к сети, а также указать переменные окружения — пользователь, пароль и база данных

**Бекенд**:

- Нужно взять образ kcoursedocker/task-7.4-back 
- Подключите к той же сети, что и базу данных
- Переменные окружения: 
PG_HOST — хост (контейнер с постгресом)
PG_USER — пользователь в постгресе
PG_PASSWORD — пароль для постгреса 
PG_DATABASE — база данных в постгресе
- Имя контейнера — backend 

**Фронтенд**:

- Нужно взять образ kcoursedocker/task-7.4-front
- Подключите к той же сети, что и базу данных с бекендом
- Прокиньте порт 80 и сходите на localhost 

В браузере вы получите нужный ответ

Решение:
```bash
docker run --rm -d --name database --net=net -p 5432:5432 -e POSTGRES_USER=docker_app -e POSTGRES_PASSWORD=docker_app -e POSTGRES_DB=docker_app_db postgres:14
docker run -it -d --net=net -e PG_HOST=database -e PG_USER=docker_app -e PG_PASSWORD=docker_app -e PG_DATABASE=docker_app_db --name backend kcoursedocker/task-7.4-back
docker run -it -d --net=net -p 80:80 kcoursedocker/task-7.4-front
```