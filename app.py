import streamlit as st
from PIL import Image
from pages.gear import cooldown

icon = Image.open("images/ico.png")
# 페이지 기본 설정
st.set_page_config(
    page_title="LSLAB",
    page_icon=icon,
    layout="centered"
)


# 페이지 링크 설정
navi = {
    "메인": [st.Page("pages/home.py", title="홈", icon="🏠", default=True)],
    "장비": [
        st.Page("pages/gear.py", title="장비", icon="🗡️"),
        ],
    "메달": [st.Page("pages/medal.py", title="메달 페이지", icon="🏅")],
}
pg = st.navigation(navi)
pg.run()