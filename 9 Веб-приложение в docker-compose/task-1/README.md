Давайте для разминки напишем **docker-compose.yaml** файл, состоящий из двух контейнеров.

Первым контейнером будет **postgres**, а со вторым будет чуть интереснее. Второй контейнер будет подниматься после постгреса, создавать в нём таблицу и сразу же останавливаться. 

Иначе говоря, мы немного необычным способом создадим таблицу в основном контейнере с базой данных. 

Для этого нам понадобится инструкция command. Именно в ней мы опишем создание таблицы.

Итак, первый сервис — **database**:

- образ —  **postgres:14**
- переменные окружения —  **POSTGRES_DB**, **POSTGRES_USER**, **POSTGRES_PASSWORD**
- вольюмы — задать вольюм и связать его с **/var/lib/postgresql/data**
- **healthcheck** — указать только **test** со значением ```["CMD-SHELL", "pg_isready", "-U", "admin"]```

## Второй сервис — **create-table**:
- образ — postgres:14
- инструкция command (см.ниже)
- зависимость от сервиса database (condition: service_healthy)
- Внутри command нужно будет указать следующее:
```bash
command: bash -c 'PGPASSWORD=admin psql -U admin --dbname todo_list -p 5432 -h database -c "CREATE TABLE IF NOT EXISTS user_table (user_id int PRIMARY KEY, username varchar(256), email varchar(256));"'
```

Где:
- ```PGPASSWORD``` — пароль (который передадите в POSTGRES_PASSWORD)
- ```-U``` — пользователь (соответствует POSTGRES_USER)
- ```--dbname``` — база данных (соответствует POSTGRES_DB)
- ```-h``` — хост (название сервиса)

Если переводить это в JSON, то должно получиться что-то в таком духе:
```JSON
{
  "version": "3",
  
  "services": {
    "database": {
      "image": "postgres:14",
      "environment": {
        "POSTGRES_DB": "todo_list",
        "POSTGRES_USER": "admin",
        "POSTGRES_PASSWORD": "admin"
      },
      "volumes": [
        "postgres:/var/lib/postgresql/data"
      ],
      "healthcheck": {
        "test": ["CMD-SHELL", "pg_isready", "-U", "admin"]
      }
    },
    
    "create-table": {
      "image": "postgres:14",
      "command": "bash -c 'PGPASSWORD=admin psql -U admin --dbname todo_list -p 5432 -h database -c \"CREATE TABLE IF NOT EXISTS user_table (user_id int PRIMARY KEY, username varchar(256), email varchar(256));\"'",
      "depends_on": {
        "database": {
          "condition": "service_healthy"
        }
      }
    }
  },
  
  "volumes": {
    "postgres": null
  }
}
```