# url 자동화하는 
# 아래 붙여 넣은 주소랑 내 api 를 concat하는 자동화 코드 만들기
import os
# os 라는 모듈이 필요해서 추가함. 
import requests
# requests 라는 모듈이 필요해서 추가함.
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') #환경 변수 안의 토큰값을 가져오세요.
URL = f'https://api.telegram.org/bot{TOKEN}'

#getUpdates: 텔레그램 서버에게 업데이트를 요청하는 함수 -> 챗봇한테 말을 걸었을 때, 누가 나한테 말을 걸었는지 정보를 알 수 있음.
# user_id, chat_id, text 등을 알 수 있음.

# json 구조로 (result 키 값안에 dictionary 형태로) 데이터를 받아옴.
# 내가 필요한 정보는 user_id -> 가져오려면 인터넷에 요청을 보내는 모듈인, requests 모듈을 사용해야 함.


# 중괄호 안에 내 토큰값을 넣는 것이 목표
# 내 토큰값은 .env 폴더 안에 들어 있음. (라이브러리가 필요함 `dotenv`. 맨 윗줄 코드)
# dotenv: 환경변수 -> .env 폴더 안의 데이터를 가지고 와서 읽어주는 라이브러리리

# print(TOKEN, URL) # 브라우저를 통해 정보 확인해봄.

# python 00_make_url.py 로 아래 터미널에서 실행해보면 토큰값을 포함한 url이 생성됨~!

res = requests.get(URL + '/getUpdates')
# getUpdates는 따로 (url을 계속해서 사용할 것이므로) 변수화 함.
# print(res.json()) # 브라우저를 통해 정보를 보는게 아니라, 터미널 창에서 바로 정보 확인하기
res_dict = res.json()
# 변수화 함

# user_id랑 text를 가져오기
user_id = res_dict['result'][0]['message']['from']['id']
# print(user_id) # [인덱스 번호 없이 확인했을 때, 마지막 괄호를 확인하면, 대괄호인 것을 확인할 수 있음. /
# -> 리스트 형태로 되어 있음. => 그래서 [0][이렇게 접근함]
text = res_dict['result'][0]['message']['text']

# 주소에 ?chat_id=7014889715&text=hello 를 붙여서 요청을 보내면, 해당 유저에게 메시지를 보낼 수 있음.
requests.get(f'{URL}/sendMessage?chat_id={user_id}&text={text}') 
# 내가 보낸 메세지를 추출하고 그걸 반환해주는 기능 (지금은 [0]이라서 첫번째 메세지가 그대로 돌아왔음)

# 서버가 필요하다 이제는!
# 요청이 들어오면, 응답을 하기 위해
# https://fastapi.tiangolo.com/ -> 서버를 만들어주는 라이브러리
# 다음주부터는 Django로 서버를 만들 예정

# pip install fastapi 로 설치하고 

# uvicorn main:app --reload 로 서버를 실행함
# main.py 파일을 실행하면, 서버가 실행됨.

# ngrok을 사용하면, 로컬 서버를 외부에서 접속할 수 있게 해줌.
# ./ngrok http 8000 -> 8000번 포트를 열어줌

# 3개의 터미널을 작동한 상태에서 실행

