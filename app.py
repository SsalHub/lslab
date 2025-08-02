import streamlit as st
from PIL import Image

# 로컬 이미지 로드
icon_img = Image.open("images/ico.png")

# 페이지 설정
st.set_page_config(
    page_title="나의 Streamlit 앱",
    page_icon=icon_img,
    layout="centered"
)

st.title("🏠 시작 페이지")
st.write("이것은 메인 페이지입니다.")

st.page_link("app.py", label="Home", icon="🏠")
st.page_link("pages/page1.py", label="➡ 두 번째 페이지로 이동", icon="👉")