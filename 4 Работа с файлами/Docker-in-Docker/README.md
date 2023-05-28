При помощи bind mount можно прокинуть сокет докера, в результате чего мы получим доступ к демону внутри контейнера.

Такое может понадобиться, например, в CI/CD (про это поговорим в последнем уроке). Если кратко — нужно уметь внутри контейнера запускать, например, сборку образа (docker build).

При этом такой подход довольно опасен, поэтому нужно быть очень аккуратным!

Подробнее можно посмотреть вот тут:
- [stackoverflow](https://stackoverflow.com/questions/35110146/can-anyone-explain-docker-sock)
- [Статья в оригинале](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)
- [ее перевод](https://habr.com/ru/company/ua-hosting/blog/488536/)

Для этого нам понадобится образ ... докера. Да, такой есть - [Ссылка](https://hub.docker.com/_/docker)

А также нужно будет сделать bind mount как раз сокета (```-v /var/run/docker.sock:/var/run/docker.sock```).
```
docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock docker
```

На хосте остановите и удалите контейнер с редисом, если он у вас поднят (```docker stop redis``` и ```docker rm redis```). В общем чтоб у вас не было конфликта имен.

Затем зайдите в этот контейнер и выполните команду ```docker run --rm -d --name redis redis```.
