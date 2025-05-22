web: gunicorn app:app --worker-class gevent --workers 3 --bind 0.0.0.0:$PORT
worker: python3 main.py
