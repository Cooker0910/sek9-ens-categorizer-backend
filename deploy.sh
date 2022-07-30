#!/usr/bin/env sh

docker stop sek9-backend

yes | docker system prune

# git pull origin main

docker build -t sek9-backend . -f Dockerfile

docker run \
  --name sek9-backend \
  --network sek9 \
  --ip 172.20.0.3 \
  --hostname sek9_backend \
  --restart unless-stopped \
  --dns=8.8.8.8 \
  -p 8000:8000 \
  -d sek9-backend

docker exec sek9-backend python manage.py runapscheduler &

yes | docker system prune
