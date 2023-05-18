# otus_hasker

## Description
Homework 6.0 from OTUS.

**TASK:** Create Q&A website, stackoverflow.com analog.

## Run deploy in Docker
- Clone repo
- Execute command
```commandline
docker compose up
```
- Open in browser http://127.0.0.1:8000/

## Run app for develop
- Clone repo
- Install requirements
```commandline
pip install -r requirements.txt
```
- Set up PostgreSQL DB
```commandline
docker run --name pg_db -p 5432:5432 -e POSTGRES_USER={{ user name }} -e POSTGRES_PASSWORD={{ pass }} -e POSTGRES_DB={{ db name }} -d postgres:15.2
```
- Make migrations (run command from directory `otus_hasker/hasker`)
```commandline
python3 manage.py migrate
```
- Run Django server
```commandline
python3 manage.py runserver
```

## Run tests in develop
```commandline
python3 manage.py test
```

## Swagger
- Open in browser http://127.0.0.1:8000/api/v1/swagger

Note: Answers list is required authentication.