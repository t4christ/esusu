#!/bin/bash
python manage.py migrate        # Apply database migrations
python manage.py collectstatic --clear --noinput # clearstatic files
python manage.py collectstatic --noinput  # collect static files
# Prepare log files and start outputting logs to stdout
# touch /srv/logs/gunicorn.log
# touch /srv/logs/access.log
# tail -n 0 -f /srv/logs/*.log &
echo Starting nginx 
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn quiz.wsgi:application \
    --name quiz \
    --bind 0.0.0.0:8009 \
    --workers 3 \
    --log-level=info 
exec service nginx start