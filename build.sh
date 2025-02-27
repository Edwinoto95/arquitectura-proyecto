# Crear archivo build.sh
echo "#!/usr/bin/env bash" > build.sh
echo "set -o errexit" >> build.sh
echo "pip install -r requirements.txt" >> build.sh
echo "python manage.py collectstatic --noinput" >> build.sh
echo "python manage.py migrate" >> build.sh