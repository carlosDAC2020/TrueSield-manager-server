# TrueShield-manager-server
Servidor de gestión de TrueShield

## Requisitos
- Python 3.11 en adelnate
## instalación

1. clone el repositorio
```
git clone https://github.com/carlosDAC2020/TrueSield-manager-server.git
```
2. Cambiar al directorio del proyecto
```
cd TrueSield-manager-server
```
3. Crear un entorno virtual 
```
python -m venv venv
```
4. Activar el entorno virtual
- En Windows
```
-\venv\Scripts\activate
```
- En Linux
```
source venv/bin/activate
```
5. instalar las dependencias
```
pip install -r requirements.txt
```
6. modificar el archivo de arranque del servidor
- Para Windows start_server.bat.
- Para Linux start_server.sh.
En este archivo se debe modificar la variable API_RSS, API_X, API_REDDIT, API_MODELS segun el host donde se ejecute el servidor de cada una de las APIs ademas de las variables correspondinets a la coneccion a la base de datos.

7. Ejecutar migraciones
```
python manage.py migrate
```
8. Ejecutar el servidor
```
python manage.py runserver
```
9. Abrir el navegador 
accedera la URL http://localhost:8000/