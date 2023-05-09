# otus_hasker

## Description
Homework 6.0 from OTUS.

**TASK:** Create Q&A website, stackoverflow.com analog.


## Set up
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

## Run
Run Django server
```commandline
python3 manage.py runserver
```

## Run tests locally
```commandline
python3 manage.py test
```

