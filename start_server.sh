#!/bin/bash

# Definir las variables de entorno
export ENVIRONMENT="dev"
export DB_NAME="app"
export DB_USER="postgres"
export DB_PASSWORD="postgres"
export DB_HOST="localhost"
export API_TOKEN_HUGGIN_FACE="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"
export MODELS_IS_OK="fail"
export API_RSS="https://0dmsfn00-8004.use2.devtunnels.ms"
export API_X="https://1gxrtlsp-8002.use2.devtunnels.ms"
export API_REDDIT="https://0dmsfn00-8004.use2.devtunnels.ms"
export API_MODELS="https://0dmsfn00-8004.use2.devtunnels.ms"

# Ejecutar el servidor de Django
python3 manage.py runserver

# Pausar el script (opcional, similar a 'pause' en Windows)
read -p "Press Enter to continue..."
