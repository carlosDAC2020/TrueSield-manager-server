@echo off

REM Comando para iniciar el contenedor de PostgreSQL
docker run -d -p "5432:5432" -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres --name DBdemo postgres:alpine


REM Entrar a la bash del container 
docker exec -it DBdemo bash