#!/bin/sh
# обновляем файлы с GH
git pull origin
git fetch --all
git reset --hard origin/main
# Собираем Docker-образ
sudo docker build -t repost-ninja-bot .
# Удаляем старый контейнер
docker stop RepostNinjaBot
docker rm RepostNinjaBot
# Запускаем контейнер
docker run -d \
 --name RepostNinjaBot \
 -e API_TOKEN=$1 \
 -e SILENT_MODE=True \
 -e REPOST_ANSWER='Р Е П О О О О О О О О О С Т ! ! !' \
repost-ninja-bot
