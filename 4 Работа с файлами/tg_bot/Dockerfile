FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY TOKEN.txt TOKEN.txt
COPY tg_bot.py tg_bot.py

ENTRYPOINT [ "python3", "tg_bot.py" ]




