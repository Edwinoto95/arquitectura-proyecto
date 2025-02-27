#!/usr/bin/env bash
set -o errexit  # Detiene si hay un error
set -o pipefail # Detecta errores en pipes
set -o nounset  # Evita variables no definidas

echo "Instalando dependencias..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear
