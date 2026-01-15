#
# 이메지 영어공부 도우미 - Gemini 이미지 분석 & 저장
#

import streamlit as st
from google import genai
from PIL import Image
import io

# 1. 페이지 설정
st.set_page_config(page_title="Gemini 이미지 분석 & 저장", layout="centered")

# 2. 세션 상태 초기화 (분석 결과를 유지하기 위함)
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 3. 사이드바 - API 키 설정
with st.sidebar:
    st.header("🔑 설정")
    # --- 2. API 키 설정 ---
    api_key = st.secrets["api_keys"].get("gemini_api_key", "")
    # api_key = st.text_input("Google Gemini API Key를 입력하세요", type="password")
    
    # 저장 버튼 디자인을 위한 안내
    st.info("분석이 완료되면 하단에 '파일로 저장' 버튼이 나타납니다.")

# 4. 메인 화면 UI
st.subheader("📸 이미지 분석 & 학습 도구 by Kevin")
# st.title("📸 이미지 분석 & 결과 저장")

uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)
    
    # 분석 버튼
    if st.button("🔍 분석 시작하기", type="primary"):
        if not api_key:
            st.error("API 키를 입력해주세요.")
        else:
            client = genai.Client(api_key=api_key)
            
            prompt = """
            이 이미지를 분석해서 다음 형식에 맞춰 한국어로 응답해줘:
            
            1. **그림 설명**: 이미지 내용 상세 설명
            2. **텍스트 번역**: 포함된 텍스트의 한국어 번역
            3. **전체 요약**: 핵심 내용 요약
            4. **중요 단어 및 학습**: 단어 3개의 [어원 설명] 및 [영어 예문]
            """
            
            with st.spinner("Gemini가 분석 중..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt, image]
                    )
                    # 결과를 세션 상태에 저장 (페이지가 새로고침되어도 유지됨)
                    st.session_state.analysis_result = response.text
                except Exception as e:
                    st.error(f"오류 발생: {e}")

# 5. 결과 출력 및 저장 버튼
if st.session_state.analysis_result:
    st.markdown("---")
    st.subheader("📝 분석 결과")
    st.markdown(st.session_state.analysis_result)
    
    # --- 저장(다운로드) 버튼 추가 ---
    st.divider()
    
    # 텍스트 파일로 내보내기 위한 데이터 준비
    result_text = st.session_state.analysis_result
    
    st.download_button(
        label="💾 분석 결과 파일로 저장하기 (.txt)",
        data=result_text,
        file_name="gemini_analysis_result.txt",
        mime="text/plain"
    )
    
    # 다시 분석하고 싶을 때를 위한 리셋 버튼
    if st.button("🔄 새로 분석하기"):
        st.session_state.analysis_result = None
        st.rerun()

# 하단 푸터
st.divider()
st.caption("© 2026 이미지 분석 비서 - Powered by Kevin")