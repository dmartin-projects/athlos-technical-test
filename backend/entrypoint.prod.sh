#!/usr/bin/env bash
set -Eeuo pipefail

echo "==> Entrypoint (ENVIRONMENT=${ENVIRONMENT:-production})"
python --version || true
which python || true
which gunicorn || true

# (Opcional) Espera simple a la BBDD si defines DB_HOST/DB_PORT
if [[ -n "${DB_HOST:-}" ]]; then
  echo "Esperando a la BBDD ${DB_HOST}:${DB_PORT:-5432} ..."
  for i in {1..60}; do
    (echo > /dev/tcp/$DB_HOST/${DB_PORT:-5432}) >/dev/null 2>&1 && break
    sleep 1
  done
fi

echo "Apply database migrations"
python manage.py migrate --noinput


echo "Starting production server with Gunicorn"
exec gunicorn "${DJANGO_WSGI_MODULE:-config.wsgi:application}" \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-2}" \
  --threads "${GUNICORN_THREADS:-4}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"

