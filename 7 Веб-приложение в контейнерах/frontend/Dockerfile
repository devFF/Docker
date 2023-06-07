FROM node:17 AS BUILD
WORKDIR /app
COPY ./todo-list/package.json ./package.json
# Устанавливаем зависимости из package.json
RUN npm i

COPY ./todo-list ./
# Запустим сборку (под капотом поднимется webpack)
RUN npm run build 
# После выполнения первого этапа у нас появятся артефакты: html, css, js и дальше мы прокидываем в NGINX

# Второй этап сборки фронтенда
FROM nginx

# Скопируем index.html в nginx
# /app/dist так как при сборке в package.json указан путь build 22 строка
COPY --from=BUILD /app/dist/index.html /nginx/static/index.html

# Скопируем css в nginx
COPY --from=BUILD /app/dist/static/css /nginx/static/

# Скопируем js в nginx
COPY --from=BUILD /app/dist/static/js /nginx/static/