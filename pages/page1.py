import streamlit as st

st.set_page_config(page_title="두 번째 페이지", page_icon="📄")

st.title("📄 두 번째 페이지")
st.write("이 페이지는 두 번째 페이지입니다.")

st.page_link("app.py", label="⬅ 홈으로 돌아가기", icon="🏠")
