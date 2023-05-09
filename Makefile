SHELL := /bin/bash

include hasker/hasker/.env

.PHONY: help
help: ## Displays help menu
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

migrate: ## Make and run migrations
	cd hasker && \
	python3 manage.py makemigrations && \
	python3 manage.py migrate

.PHONY: run
run: ## Run the Django server
	cd hasker && \
	sudo python3 manage.py runserver 0.0.0.0:80

prod: install migrate run ## Install requirements, apply migrations, then start development server