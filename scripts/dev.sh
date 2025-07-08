#!/bin/bash

echo "🔄 Parando contenedores anteriores..."
docker-compose down

echo "🚀 Levantando base de datos (PostgreSQL)..."
docker-compose up -d db

echo "⏳ Esperando a que la base de datos esté lista..."
sleep 5

echo "📜 Ejecutando migraciones..."
./scripts/migration.sh initial || echo "⚠️ Ya aplicadas o sin cambios"

echo "🚀 Levantando aplicación FastAPI..."
docker-compose up -d web

echo "✅ Entorno levantado: http://localhost:8000/docs"

echo "📡 Mostrando logs en tiempo real del contenedor web:"
docker-compose logs -f web
