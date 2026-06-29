import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime
from telegram import Bot

load_dotenv()

SOFRANO_ID       = os.getenv('SOFRANO_ID')
SOFRANO_PW       = os.getenv('SOFRANO_PW')
TELEGRAM_TOKEN   = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def login():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
    login_data = {
        'member_id': SOFRANO_ID,
        'member_passwd': SOFRANO_PW,
    }
    res = session.post(
        'https://sofrano.com/exec/front/Member/login/',
        data=login_data,
        allow_redirects=True
    )
    print(f'[LOGIN] status: {res.status_code}')
    return session


def check_attendance(session):
    today = datetime.now()
    url = f'https://sofrano.com/attend/stamp.html?year={today.year}&month={today.month}'
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    today_day = str(today.day)
    table = soup.find('table')
    if not table:
        print('[CHECK] table not found')
        return 'unknown'

    for td in table.find_all('td'):
        text = td.get_text(strip=True)
        if text == today_day or text.startswith(today_day + ' '):
            img = td.find('img')
            if img:
                alt = img.get('alt', '')
                print(f'[CHECK] day {today_day} alt={alt}')
                if alt == '' or 'Off' in img.get('src','') or 'attendOff' in img.get('src',''):
                    return 'not_attended'
                else:
                    return 'attended'

    print(f'[CHECK] day {today_day} not found in table')
    return 'unknown'


async def send_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print('[TELEGRAM] sent')


def main():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] sofrano attend check start...')

    session = login()
    status = check_attendance(session)
    today_str = datetime.now().strftime('%Y-%m-%d')

    if status == 'not_attended':
        message = (
            f'[{today_str}]\n'
            'Sofrano attendance check not done!\n'
            'https://sofrano.com/attend/stamp.html'
        )
        asyncio.run(send_telegram(message))
    elif status == 'attended':
        print('[DONE] already attended. no alert.')
    else:
        message = (
            f'[{today_str}]\n'
            'Could not verify sofrano attendance.\n'
            'Please check: https://sofrano.com/attend/stamp.html'
        )
        asyncio.run(send_telegram(message))


if __name__ == '__main__':
    main()
