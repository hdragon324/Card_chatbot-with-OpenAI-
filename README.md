# Card_chatbot-with-OpenAI-

chat_bot.py가 메인 파일입니다.

터미널에서 아래 패키지부터 설치 하십시오
pip install streamlit selenium beautifulsoup4 requests tqdm openai langchain

프롬프트나 터미널에서 chat_bot.py 가 들어있는 파일 경로에서 streamlit run chat_bot.py 를 실행 하십시오.

# 프로젝트 이름

이 프로젝트는 OpenAI API 을 위한 프로젝트입니다. 이 프로젝트는 다양한 패키지를 사용하여 웹 크롤링, 데이터 분석, 모델 학습 등을 구현합니다.

## 파일 구조

프로젝트의 파일 구조는 다음과 같습니다:

CARD_CHATBOT-WITH-OPENAI-/
├── chat_bot.py                         # Streamlit 애플리케이션 실행 파일
├── Card_chatbot.ipynb                  # 챗봇 모델 생성 및 비교 평가 파일
├── card_img/                           # 카드 이미지 폴더
│   ├── check_card/                     # 체크 카드 이미지 폴더
│   ├── credit_card/                    # 신용 카드 이미지 폴더
├── utils/                              # 데이터 크롤링 및 챗봇에 사용하는 크롤링 및 추천 함수 폴더
│   ├── __pycache/                      # 캐시 폴더
│   ├── crawl.py                        # 크롤링 함수
│   └── recommend.py                    # 카드 추천 챗봇 함수
├── VectorStores/                       # FAISS, E5를 사용한 유사도 기반 VectorDB 폴더
│   ├── check_card_embeddings.index     # 체크카드의 임베딩 파일
│   └── credit_card_embeddings.index    # 신용카드의 임베딩 파일
└── README.md                           # 프로젝트 설명 파일




