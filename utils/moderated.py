import streamlit as st
from langchain.chains import LLMChain
from openai import OpenAI

# ------------------- 사전 설정 부분 -------------------
# 사용자의 질의에 대해 적절한 컨텐츠인지 확인하는 사용자 정의 함수 (moderation 모델 적용)
def moderation_message(message):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.moderations.create(model='text-moderation-latest',
                                         input=message)
    
    moderation_result = response.results[0]

    # 메시지가 유해하다면
    if moderation_result.flagged:
        category_type = dict(moderation_result.categories)
        categories = [k for k,v in category_type.items() if v == True]
        return False, categories
    
    return True, None
    # None은 없어도 되지만 return이 여러개인 함수의 경우 반환 형태를 일정하게 해주기 위함


# LLMChain 클래스를 상속받은 사용자 정의 클래스인 ModeratedLLMChain 선언
# (LLMChain 내부에서 Moderatrion을 지원하지 않기 때문에 상속받아서 추가코드 작성)\
class ModeratredLLMChain(LLMChain):
    # 전달 메세지가 적절한지 확인하기 위해 moderate_message함수를 호출하고 응답 생성 및 상황에 따른 출력 문구 작성
    def moderate_and_generate(self, user_input):
        is_safe, categories = moderation_message(user_input)
        # moderate_message의 결과로 유해하다고 판단되면 is_safe에는 False가 반환될 것임
        # 유해한 경우에 실행될 코드
        if not is_safe :
            st.write(f'사용자의 메시지가 부적절하여 차단되었습니다. : {categories}')
            return ""
            # st.write는 값의 반환없이 웹에 출력만 시키므로 return 에는 None이 들어가서 동작하게 되는 데 None이 웹으로 출력되는 것을 방지하기 위해 빈 문자열을 반환

        # 상속받은 LLMChain클래스의 predict 메소드로 응답 실행
        response = self.predict(question=user_input)

        # 모델 응답에 대한 moderation
        is_safe_ai, categories_ai = moderation_message(response)
        if not is_safe_ai:
            st.write(f"AI 응답이 부적절하여 차단되었습니다 : {categories_ai}")
            return ""
        
        return response