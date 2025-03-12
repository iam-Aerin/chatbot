# 각 기능을 쪼개서 구성
# https://finance.naver.com/sise/ 네이버 페이 증권 코스피 값 가져오기

import requests
from bs4 import BeautifulSoup
from openai import OpenAI

from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'

    res =  requests.get(KOSPI_URL)
    # 내가 준 url 에 있는 html 코드를 가져오는 기능
    print(res.text) # 가져온 html 코드를 출력하는 기능

    selector = '#KOSPI_now'
    # url (화면에서) 코드 inspect를 하고 copy selector 를 해서 필요한 id 값을 가져옴
    # HTML 코드를 읽게 하기 위해 bs4를 사용함

    soup = BeautifulSoup(res.text, 'html.parser')
    # 가져온 html 코드를 파싱하는 기능 (지금 내 데이터가 html이라서 html.parser를 사용함) 
    kospi  = soup.select_one(selector)
    # bs4의 기능 select_one => 규칙을 지정해줌. 

    return(kospi.text)

def openai(api_key, user_input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': ':You are a helpful assistant, be poite and informative.'},
            {'role': 'user', 'content': user_input}

        ]
    )
    return(completion.choices[0].message.content)

def langchain(user_input):
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = InMemoryVectorStore(embeddings)

    # 1. Load a document
    # 참고할 문서 저장하는 공간
    loader = WebBaseLoader(
        web_paths=(
            'https://namu.wiki/w/BOYNEXTDOOR',
        )
    )
    docs = loader.load()

    # 2. Split the document into sentences
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    all_splits = text_splitter.split_documents(docs)
##
    # 3. Store the sentences in the vector store
    _ = vector_store.add_documents(documents=all_splits)

    # 4. Retrieve the most similar sentences
    # 내가 가진 데이터를 검색하는 단계
    prompt = hub.pull('rlm/rag-prompt')
    # langchain에서 설정해놓은 prompt를 가져옴 (규격-> 어떻게 저장한 데이터를 가져올지/ 대답할지에 대한 규격격)
    retrieved_docs = vector_store.similarity_search(user_input)
    docs_content = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    prompt = prompt.invoke({'question': user_input, 'context': docs_content})
    answer = llm.invoke(prompt).content

    return answer