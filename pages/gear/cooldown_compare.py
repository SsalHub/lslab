import streamlit as st

def renderGearInfo(parent, index: int):
    if "selected" not in st.session_state or len(st.session_state.selected) < index + 1:
        with parent:
            st.image("images/none.png")
            st.subheader("선택된 장비 없음")
    with parent:
        st.image(f"")

def render(data):
    main_container = st.container(horizontal_alignment="center")
    with main_container.container(border=True, width=600, horizontal=True, horizontal_alignment="center"):
        if "selected" not in st.session_state:
            st.image("images/none.png")
            st.title("선택된 장비 없음")

            