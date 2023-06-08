**Docker-compose** - это программа, которая позволяет работать с многоконтейнерными приложениями docker. В специальном файле **docker-compose.yaml** мы просто пишем инструкции как должно подняться приложение. Даже при наших простых задачах, команды для запуска проекта оказываются очень громоздкими. Можем упростить себе жизнь.
# YAML
Формат, в котором описываются инструкции для **docker-compose** называется **YAML**. Он используется не только для docker-compose, также может быть использован для **kubernetes** и прочее. YAML можно назвать языком хранения данных.
Он имеет легкий синтаксис:
- отступы
- ключ-значение
- последовательности (аналог списков/массивов)
- словари

Для работы подготовим парсер YAML-файлов:
```python
import yaml

if __name__ == '__main__':
    with open("yaml_file.yaml) as f:
        templates = yaml.safe_load(f)

    print(templates)
```

Напишем первый YAML-файл:
```YAML
# Зададим ключ и два значения через пробел:
name: Peter Olga
# Parser: {'name': 'Peter Olga'}

# Зададим ключ и два значения через пробел (2-й вариант):
name:
    Peter 
    Olga
# Parser: {'name': 'Peter Olga'}

# Зададим ключ и два значения через перенос строки:
name: |
    Peter 
    Olga
# Parser: {'name': 'Peter\nOlga\n'}

# Параграф:
name: >
    Peter 
    Olga

# Сделаем список:
name:
    - Peter 
    - Olga
# Parser: {'name': ['Peter', 'Olga']}

# Сделаем список с словарями:
name:
    - Peter: 
      Olga:
# Parser: {'name': [{'Peter': None}, {'Olga': None}]}

# А как здесь объединить их в один словарь + создадим другой)?
name:
    - Peter: 12
      Olga: 13

    - Oleg: 7
      Julia: 2
# Parser: {'name': [{'Peter': 12, 'Olga': 13}, {'Oleg': 7, 'Julia': 2}]}
```


# docker-compose
Airflow - планировщик ETL(миграция данных из одного хранилища в другое) (EXTRACT - выгружаем данные из БД, TRANSFORM - обрабатываем их, LOAD - загружаем их в clickhouse) процессов.

Рассмотрим docker-compose на примере этого сервиса. Для этого скачаем docker-compose Airflow следующей командой:
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.1/docker-compose.yaml'
```

Видим интересный синтаксис ```&``` и ```<<: *``` - это якорь и ссылка на якорь. Посмотрим применение: (Случай- у всех джунов одинаковая ЗП)
```YAML
# Могли написать так
team:
    backend:
        - Peter:
            position: junior
            salary: 55000
        - Olga:
            position: junior
            salary: 55000

# Но правильне было бы так:
# шаблон
junior:
    &junior
    position:junior
    salary:55000

# Вызываем этот шаблон:
team:
    backend:
        - Peter:
            <<: *junior
        - Olga:
            <<: *junior
```

Идем дальше, видим некие сервисы и вольюмы (в конце). Сервисы - это и есть наши контейнеры.
```YAML
image: postgres:13 # задает образ
enviroment:
    POSTGRES_USER: airflow # задает переменные окружения
volumes:
    - postgres-db-volume:/var/lib/postgresql/data # задает том
expose:
    - 5432 # указываем порт для приложения
ports:
    - 5432:5432 # пробрасываем порт
```
# Разворачиваем Airflow
Ссылка на документацию по разворачиваю Airflow - [тык](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
Поднимем одной командой 5 контейнеров:
```bash
docker-compose up
```

Остановим их Ctrl+C. Можем увидеть наши контейнеры как через ```docker ps -a```, так и через ```docker-compose ps```. 

Остановим и удалим все контейнеры от docker-compose: 
```bash
docker-compose down
```

Поднимем Airflow еще раз, но скроем логи:
```bash
docker-compose up -d
```

Посмотреть документацию:
```bash
docker-compose --help
docker-compose exec --help
```

## Команды
- ```docker-compose ps``` — список контейнеров (ссылка)

- ```docker-compose up``` — поднять приложение (ссылка)

      - - ```docker-compose up <сервис>``` — поднять конкретный контейнер

      - - ```docker-compose up -d``` — поднять контейнеры в фоновом режиме

      - - ```docker-compose  -f docker-compose.dev.yml up``` — указать docker-compose.yaml файл (ссылка)

- ```docker-compose stop``` — остановить поднятые контейнеры (ссылка)

- ```docker-compose start``` — запустить остановленные контейнеры (ссылка)

- ```docker-compose down``` — остановить и удалить контейнеры и сеть  (ссылка)
