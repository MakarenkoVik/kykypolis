VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python3
SHELL := /bin/bash


.PHONY: venv
venv: ## Создать виртуальное окружение
	source $(BIN)/activate

.PHONY: install
install: venv ## установить зависимости
	$(BIN)/pip install --upgrade -r requirements.txt

freeze: ## сохранить зависимости
	$(BIN)/pip freeze > requirements.txt

.PHONY: migrate
migrate: ## зхапустить миграции
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

.PHONY: build_translations
build_translations: ## пересобрать первод
	cd service && django-admin makemessages -l ru  && django-admin makemessages -l en && cd ..
	cd users && django-admin makemessages -l ru  && django-admin makemessages -l en && cd ..
	django-admin compilemessages

.PHONY: run
run: ## запустить проект
	$(PYTHON) manage.py runserver

start: install migrate build_translations run
