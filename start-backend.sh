source ~/virtualenvs/auricle/bin/activate && cd backend && gunicorn --bind 0.0.0.0:8000 --workers 4 auricle.wsgi:application