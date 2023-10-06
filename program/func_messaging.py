import requests
from constants import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


# Send Message
def send_message(message):
    bot_token = TELEGRAM_TOKEN
    chat_id = TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    res = requests.get(url)
    if res.status_code == 200:
        return "sent"
    else:
        return "failed"
