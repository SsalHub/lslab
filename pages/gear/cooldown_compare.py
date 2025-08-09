import streamlit as st

def renderGearInfo(parent, index: int):
    if "selected" not in st.session_state or len(st.session_state.selected) < index + 1:
        with parent:
            st.image("images/none.png")
            st.subheader("선택된 장비 없음")

def render(gear_list):
    main_container = st.container(border=True, horizontal=True, horizontal_alignment="center")
    selected_0, selected_1 = st.container(), st.container()
    renderGearInfo(selected_0, 0)
    renderGearInfo(selected_1, 1)