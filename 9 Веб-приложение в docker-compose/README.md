# Инструкции docker-compose
- versions: версия (будем использовать 3ю)
- services: наши контейнеры
- volumes: вольюмы (томы)
- networks: сеть

## volumes
```YAML
# Можем не указывать имя БД, поулчим имя: имя папки + имя бд
volumes:
    todo_db:

# Или укажем имя явно
volumes:
    todo_db:
        name: todo_db
```

## network
С сетью аналогично:
```YAML
networks:
    todo_net:
        name: todo_net
```

Важные доп. функции docker-compose:
- ```restart``` и ```restart_policy``` - перезапуск контейнера
- ```replicas``` - количество копий контейнера, которые нужно поднять
- ```depends_on``` - выставляет зависимость одного контейнера от другого
- ```healthcheck``` - запустить некую проверку после поднятия контейнера (например БД при поднятии не сразу может быть готова к работе)


# Веб приложение в docker-compose
см docker-compose.yaml
# Расширяем docker-compose файл
см docker-compose.yaml
После указания зависимостей у нас установился порядок запуска контейнеров.
# Сокращаем docker-compose файл

# Инструкции