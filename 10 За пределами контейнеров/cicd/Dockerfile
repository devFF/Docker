FROM python:3.8

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

COPY src/app.py ./app.py
COPY src/wsgi.py ./wsgi.py

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app" ]