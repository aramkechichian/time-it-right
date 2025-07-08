#!/bin/bash
echo "🔍 Running tests with pytest inside Docker..."
docker-compose exec -T web bash -c "export PYTHONPATH=/app && pytest -vv --tb=long -W ignore tests/" | tee logs/pytest_output.log