# syntax=docker/dockerfile:1

FROM postgres:15

COPY deploy/db/init-db.sh /docker-entrypoint-initdb.d/01init.sh

COPY deploy/db/pg.conf /etc/postgresql/postgresql.conf

EXPOSE 5432