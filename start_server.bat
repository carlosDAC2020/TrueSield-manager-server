@echo off

set ENVIRONMENT=dev
set DB_NAME=app
set DB_USER=postgres
set DB_PASSWORD=postgres
set DB_HOST=localhost

py manage.py runserver

pause

