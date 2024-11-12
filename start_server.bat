@echo off

set ENVIRONMENT=dev
set DB_NAME=app
set DB_USER=postgres
set DB_PASSWORD=postgres
set DB_HOST=localhost
set API_TOKEN_HUGGIN_FACE=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
set MODELS_IS_OK=fail
set API_RSS=https://0dmsfn00-8004.use2.devtunnels.ms
set API_X=https://1gxrtlsp-8002.use2.devtunnels.ms
set API_REDDIT=https://0dmsfn00-8004.use2.devtunnels.ms
set API_MODELS=https://0dmsfn00-8004.use2.devtunnels.ms

py manage.py runserver

pause

