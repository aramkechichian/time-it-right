#!/bin/bash

NAME=${1:-auto}

echo "📦 Generando migración Alembic: $NAME..."
docker-compose run --rm web alembic revision --autogenerate -m "$NAME"

echo "🚀 Aplicando migraciones..."
docker-compose run --rm web alembic upgrade head

echo "✅ Migraciones aplicadas con éxito."
