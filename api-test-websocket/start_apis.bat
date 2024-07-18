@echo off

:: Ruta de la aplicación Flask
set "app_path=main.py"  :: Reemplaza con la ruta de tu aplicación Flask


:: Puerto en el que se ejecutará el servidor
set "port1=8001"  :: Puedes cambiar este puerto según tus necesidades
set "port2=8002" 
set "port3=8003" 

:: Función para iniciar el servidor Flask
:start_flask
start python "%app_path%"  "%port1%"
echo Iniciando servidor Flask en el puerto %port1%...
start python "%app_path%"  "%port2%"
echo Iniciando servidor Flask en el puerto %port2%...
start python "%app_path%"  "%port3%"
echo Iniciando servidor Flask en el puerto %port3%...

goto :EOF

:: Iniciar el servidor Flask
call :start_flask

:: Mantener el script en ejecución hasta que se presione Ctrl+C
echo Presiona Ctrl+C para detener el servidor Flask.
timeout /t -1