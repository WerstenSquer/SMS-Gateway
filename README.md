# Run the server with: 
uvicorn main:app --reload
# Run the celery workers with: 
celery -A sender.celery worker -l info -P gevent --queues=mailing
celery -A sender.celery worker -l info -P gevent --queues=sending

