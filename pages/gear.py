import streamlit as st
import json
from pages.gear import cooldown, cooldown_compare


st.title("장비 페이지")
st.write("이용할 기능을 선택하세요.")

with open('data/gears.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
tabs = st.tabs(["⏳쿨타임 조회", "↔️쿨타임 비교"])
with tabs[0]:
    cooldown.render(data['gear'])
with tabs[1]:
    cooldown_compare.render(data['gear'])