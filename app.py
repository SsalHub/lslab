import streamlit as st
from PIL import Image

# 로컬 이미지 로드
icon_img = Image.open("images/ico.png")
# 페이지 기본 설정
st.set_page_config(
    page_title="LSLAB",
    page_icon=icon_img,
    layout="centered"
)


# 페이지 링크 설정
navi = [
    st.Page("pages/home.py", title="홈", icon="🏠", default=True),
    st.Page("pages/gear.py", title="장비 페이지", icon="🗡️"),
    st.Page("pages/medal.py", title="메달 페이지", icon="🏅"),
]
pg = st.navigation(navi)
pg.run()