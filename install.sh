#!/bin/sh

# Собираем Docker-образ
sudo docker build -t repost-ninja-bot .
# Запускаем контейнер
docker run -d \
 --name RepostNinjaBot \
 -e API_TOKEN=$1 \
 -e SILENT_MODE=True \
 -e REPOST_ANSWER='Р Е П О О О О О О О О О С Т ! ! !' \
repost-ninja-bot
