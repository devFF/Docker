## Поднимаем Postgres
```bash
docker run --rm -d \
  --name database \
  --net=back_net \
  -e POSTGRES_USER=docker_app \
  -e POSTGRES_PASSWORD=docker_app \
  -e POSTGRES_DB=docker_app_db \
  postgres:14
```

## Создаем таблицу Postgres
У Postgres есть своя консоль для управления БД - psql.
``` bash
docker exec -it database psql --username docker_app --dbname docker_app_db
```
Внутри контейнера с postgres создаем таблицу:
Можно вводить построчно, так как инструкция закрывается через ```;```
```SQL
CREATE TABLE app_table (
    id     text NOT NULL,
    text   text NOT NULL,
    status text NOT NULL
);
```
Проверим нашу таблицу:
```SQL
SELECT * FROM app_table
```

## Поднимаем backend
Через переменную окружения укажем имя контейнера с БД
``` bash
docker run --rm -d \
  --name backend \
  --net=back_net \
  -p 8000:8000 \
  -e HOST=database \
  6_back
```

## Делаем запросы к бэкенду
```bash
curl -X PUT localhost:8000/api -H 'Content-Type: application/json' -d '{"text":"Buy cheese","status":"active"}'
curl localhost:8000/api
```