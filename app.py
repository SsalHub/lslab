import streamlit as st
from PIL import Image

# 로컬 이미지 로드
icon_img = Image.open("images/ico.png")

# 페이지 설정
st.set_page_config(
    page_title="LSLAB",
    page_icon=icon_img,
    layout="centered"
)

st.title("LSLAB")
st.write("LSLAB에서 이용할 기능을 선택하세요")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/gear.py", label="장비 페이지", icon="🗡️")
with col2:
    st.page_link("pages/medal.py", label="메달 페이지", icon="🏅")