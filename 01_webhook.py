# setWebhook URL 만들기
# https://api.telegram.org/bot<token>/setWebhook?url=<url>

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') #환경 변수 안의 토큰값을 가져오세요.
NGROK_URL = os.getenv('NGROK_URL') #환경 변수 안의 ngrok 주소를 가져오세요.
# .env 파일에 있는 두개의 변수를 가져오세요. 

URL = f'https://api.telegram.org/bot{TOKEN}/setWebhook'

# print(TOKEN)
# print(NGROK_URL)
print(f'{URL}?url={NGROK_URL}')  