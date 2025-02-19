from utils.recommend import recommend_my_model_test
import json

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from openai import OpenAI

# ------------------- 사전 설정 부분 -------------------
chat_model = ChatOpenAI(model_name='gpt-3.5-turbo',
                        api_key=st.secrets['OPENAI_API_KEY'],
                        temperature=0.5)

my_prompt = PromptTemplate(input_variables=['chat_history', 'question'],
                        template='''You are an AI assistant. You are currently having a converasation with a human. Answer the Question.
                        chat_history : {chat_history},
                        Human : {question},
                        AI_assistant:''')

# 일반적인 코드에서는 memory개체를 생성하면 대화 내용들을 자동으로 기억하지만 streamlit에서는 웹에서 요청, 응답을 수행하기 때문에
# 따로 저장해두지 않으면 다 초기화 됨

# session_state에 처음부터 값을 저장하지 않고 if not in을 사용하는 이유는 코드를 재 실행 시켰을 경우 기존 session_state에 저장된 값이
# 초기화 되는 것을 방지하기 위해
if 'pre_memory' not in st.session_state:
    st.session_state.pre_memory = ConversationBufferMemory(memory_key='chat_history',
                                                           return_messages=True)
    
llm_chain = LLMChain(llm=chat_model,
                     prompt=my_prompt,
                     # .pre_memory로 접근하면 세션으로 관리되는 CBMemory객체가 입력됨
                     memory=st.session_state.pre_memory)


# LLM에 요청하고 응답 받을 수 있는 chat 형태로 messages를 관리
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role':'assistant','content':'안녕하세요, 저는 소비자의 소비 습관에 맞춰 최적의 카드를 추천해주는 CARA (Card Advisor & Recommendation AI) 입니다.'}]

# ------------------- ----------------- --------------
# ------------------- 웹 표시 부분 --------------------
# CSS 스타일 정의
st.markdown(
    """
    <style>
    .title {
        font-size: 70px;
        font-weight: bold;
        color: #003366; /* 진한 남색 */
        text-align: center;
        padding: 15px;
        border: 4px solid #003366; /* 두꺼운 테두리 */
        border-radius: 12px;
        background: linear-gradient(135deg, #4A90E2, #A0C4FF); /* 파란색 계열 그라디언트 */
        box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.3); /* 더 강한 그림자 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 제목 표시
st.markdown('<p class="title">💳 카드 추천 챗봇 : CARA 💳</p>', unsafe_allow_html=True)


# 반복문으로 session_state.messages에 있는 모든 대화 기록에 접근
for message in st.session_state.messages : 
    # chat_message : 메시지의 발신자 role에 따라 UI를 구분하여 출력
    #               assistant, user는 디폴트로 설정되어 있으며 다른 role을 추가하려면 HTML코드 작성이 필요
    with st.chat_message(message['role']) :
        st.write(message['content'])

# chat_input : 채팅 메시지 입력 UI가 생성되며 사용자가 입력한 텍스트를 받아오는 함수
user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({'role':'user','content':user_prompt})
    with st.chat_message('user'): # user 형태로 메시지 창 UI 출력
        st.write(user_prompt)     # 사용자가 입력한 질문 출력


# 마지막 메시지의 role이 assistant가 아니라면 새로운 답변을 생성하고 session_state에 추가
# (assistant가 본인의 응답에도 계속 대답하는 자문자답을 방지하기 위해)
if st.session_state.messages[-1]['role'] != 'assistant' :
    # assistant 메시지 UI 생성
    with st.chat_message('assistant') :
        # AI가 응답을 생성하는 동안 로딩 애니메이션이 실행됨
        with st.spinner('Loading...') :
            try:
                # 사용자가 채팅 메시지를 추천과 관련된 이야기를 했다면
                if any(keyword in user_prompt.lower() for keyword in ["카드추천", "카드 추천", "추천"]):

                    # 응답과 카드 코드를 반환
                    ai_response, card_code = recommend_my_model_test(user_prompt)

                    # 카드 이미지를 ai_response 상단에 출력함
                    image_path = f"card_image/{card_code}card.png"
                    st.image(image_path, width=300)
                    st.write(f'- **카드고릴라 URL** : https://www.card-gorilla.com/card/detail/{card_code}')
                
                # 사용자가 채팅 메시지로 역할에 관해 물어봤다면
                elif any(keyword in user_prompt.lower() for keyword in ["역할", "role"]):
                    ai_response = '저의 역할은 소비자 습관에 맞춰 카드를 추천하는 봇입니다.'
                else:
                    ai_response = llm_chain.predict(question=user_prompt)
                st.write(ai_response)
                # 모델의 응답도 세션의 messages에 추가하여 관리
                st.session_state.messages.append({'role':'assistant','content':ai_response})
            except Exception as e:
                st.error(f'LLM 에러 발생 : {e}')