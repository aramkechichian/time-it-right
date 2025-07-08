#!/bin/bash
echo "🔍 Corriendo Test dentro de Docker..."
docker-compose exec -T web bash -c "export PYTHONPATH=/app && pytest -vv --tb=long -W ignore tests/" | tee logs/pytest_output.log