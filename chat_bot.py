from utils.recommend import recommend_my_model_test
import json

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from openai import OpenAI


with open('data/check_card_info-ver-4.json', 'r', encoding='utf-8') as json_file:
    check_card_data = json.load(json_file)

with open('data/credit_card_info-ver-4.json', 'r', encoding='utf-8') as json_file:
    credit_card_data = json.load(json_file)
    
user_content = '아무 카드나 추천'
print(recommend_my_model_test(user_content, check_card_data, credit_card_data))