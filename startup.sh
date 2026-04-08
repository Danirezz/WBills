#!/bin/bash
<<<<<<< HEAD

# Script de inicio para FastAPI en Azure App Service

PORT=${PORT:-8000}

echo "=========================================="
echo "🚀 Iniciando FastAPI en el puerto $PORT"
echo "📁 Archivo principal: app.py"
echo "🔧 Instancia de FastAPI: app"
echo "=========================================="

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT
=======
PORT=${PORT:-8000}
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
>>>>>>> 589616a (Cambios)
