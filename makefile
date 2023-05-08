VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python3
SHELL := /bin/bash


.PHONY: venv
venv: ## Создать виртуальное окружение
	source $(BIN)/activate

.PHONY: install
install: venv ## Установить зависимости
	$(BIN)/pip install --upgrade -r requirements.txt

freeze: ## Сохранить зависимости
	$(BIN)/pip freeze > requirements.txt

.PHONY: migrate
migrate: ## Запустить миграции
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

.PHONY: build_translations
build_translations: ## Пересобрать первод
	cd service && django-admin makemessages -l ru  && django-admin makemessages -l en && django-admin compilemessages && cd ..
	cd users && django-admin makemessages -l ru  && django-admin makemessages -l en && django-admin compilemessages && cd ..

.PHONY: format
format: ## Flake black isort
	$(BIN)/black ./
	$(BIN)/isort --recursive ./service && $(BIN)/isort --recursive ./users
	$(BIN)/flake8 ./service && $(BIN)/flake8 ./users

.PHONY: run
run: ## Запустить проект
	$(PYTHON) manage.py runserver

start: install migrate format build_translations run
