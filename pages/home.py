import streamlit as st
from PIL import Image


st.title("LSLAB")
st.write("LSLAB에서 이용할 기능을 선택하세요")

st.page_link("pages/gear.py", label="장비 페이지 바로가기", icon="🗡️")
st.page_link("pages/medal.py", label="메달 페이지 바로가기", icon="🏅")