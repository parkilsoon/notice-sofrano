# notice-sofrano

Sofrano Mall attendance check notifier via Telegram.
Runs daily on Linux via cron and sends a Telegram alert if you have not checked in yet.

## Files

| File | Description |
|------|-------------|
| `attend.py` | Main script: login, check attendance, send Telegram alert |
| `.env.example` | Template for your credentials (copy to `.env`) |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Ignores `.env` and other local files |

## Setup

### 1. Clone & install

```bash
git clone https://github.com/parkilsoon/notice-sofrano.git
cd notice-sofrano
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure .env

```bash
cp .env.example .env
nano .env   # fill in your credentials
```

### 3. Test run

```bash
python3 attend.py
```

### 4. Register cron job (daily at 9:00 AM)

```bash
crontab -e
```

Add this line (replace USERNAME with your Linux username):

```
0 9 * * * /home/USERNAME/notice-sofrano/venv/bin/python3 /home/USERNAME/notice-sofrano/attend.py >> /home/USERNAME/notice-sofrano/log.txt 2>&1
```

## How it works

1. Logs in to sofrano.com with your credentials
2. Checks the attendance calendar for today
3. If not attended: sends a Telegram message with a direct link
4. If already attended: exits silently

## Telegram Bot Setup

1. Search `@BotFather` on Telegram
2. Send `/newbot` and follow instructions to get your `TELEGRAM_TOKEN`
3. Send any message to your new bot
4. Visit `https://api.telegram.org/bot[TOKEN]/getUpdates` to find your `TELEGRAM_CHAT_ID`
