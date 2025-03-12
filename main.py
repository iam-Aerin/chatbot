# 챗봇에 응답을 해주는 기능
# 모듈화 해놓은 utils.py를 가져와서 사용함.

# https://platform.openai.com/docs/overview?lang=python -> chatgpt api 사용할 python 코드 가져오기 

import os
import requests
import random
from dotenv import load_dotenv

from typing import Union
from fastapi import FastAPI, Request

from utils import kospi, openai, langchain

app = FastAPI()

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

@app.post('/')
async def read_root(request: Request):
    body = await request.json()
    # print(body)

    user_id = body['message']['chat']['id']
    text = body['message']['text']

    # 사용자가 만든 (입력한) 텍스트를 분기 처리
    # 만약 사용자가 /를 붙이고 lotto를 입력하면, 1~45까지의 숫자 6개를 랜덤으로 뽑아서 출력

    if text[0] == '/':
        if text == '/lotto':
            numbers = random.sample(range(1, 46), 6)
            output = str(sorted(numbers))
        elif text == '/kospi':
            output = kospi() 
    else:
        # output = openai(OPENAI_API_KEY, text) # else 문에 (utils에서 가져온 chatgpt api를 사용할 때 사용할 것임.)
        output = langchain(text)

    requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={output}')
    
    return body

# fastapi의 main 문서를 복사 붙여 넣기 해 온 코드임. 
# 어떤 정보를 가지고 왔는지를 찾는 과정

# async - await 함수: 비동기 함수
# -> 함수가 실행되는 동안 다른 함수를 실행할 수 있음.
