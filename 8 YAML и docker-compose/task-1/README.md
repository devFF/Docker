YAML файлы действительно очень часто используются, поэтому давайте их немного попишем.

Возьмем простой YAML файлик, который будет содержать информацию о постгресе и кликхаусе. 

Для начала задайте 2 ключа — **postgres** и **clickhouse**.

В postgres нужно указать словарь, который будет иметь следующие значения:

- user — postgres_app_user
- password — postgres_app_password
- host — postgres_host
- port — 5432

В clickhouse также словарь, но уже со значениями:

- host — clickhouse_host
- user — clickhouse_app_user
- db — clickhouse_app_db
- password — clickhouse_app_password

Если переводить это в JSON, то должно получиться что-то в таком духе:
```json
{
  "clickhouse": {
    "db": "clickhouse_app_db",
    "host": "clickhouse_host",
    "password": "clickhouse_app_password",
    "user": "clickhouse_app_user"
  },
  "postgres": {
    "host": "postgres_host",
    "password": "postgres_app_password",
    "port": 5432,
    "user": "postgres_app_user"
  }
}
```
