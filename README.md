# RepostNinjaBot
 
# Quick start

1. Get your bot token via BotFather
2. Get Docker
3. Clone repository
4. Set permissions
3. Run install script using `YOUR_BOT_TOKEN` you got at step 1

```
git clone https://github.com/glebsterx/RepostNinjaBot.git
cd RepostNinjaBot
sudo chmod +x install.sh
sudo ./install.sh YOUR_BOT_TOKEN
```

# Container settings

 - API_TOKEN -- (string) your bot token
 - SILENT_MODE -- (bool) silent mode switch
 - REPOST_ANSWER -- (string) answer to any reposted message

## Серверы (прод / тест)

_Обновлено 2026-09-20. Общая схема — `/data/homelab/docs/naming-convention.md`._

- **Прод:** LXC `apps-home-01` (192.168.0.11, `ssh apps`, код в `/data/RepostNinjaBot`) — целевой, сейчас нигде не запущен
- **Тест/dev:** LXC `apps-dev-home-01` (192.168.0.18, `ssh apps-dev`, VMID 207 на pve-home-02) — целевой
