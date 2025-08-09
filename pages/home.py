import streamlit as st

def render():
    st.title("LSLAB")
    st.write("LSLAB에서 이용할 기능을 선택하세요.")
    st.divider()

    cols = st.columns([1, 4, 4, 1])
    link_container = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center")
    
    with link_container.container(border=True, horizontal_alignment="center", vertical_alignment="center"):
        st.image("images/gear_ico.png", use_container_width=True)
        if st.button('장비 페이지', icon='🗡️', type="tertiary", use_container_width=True):
            st.switch_page("pages/gear.py")
    with link_container.container(border=True, horizontal_alignment="center", vertical_alignment="center"):
        st.image("images/medal_ico.png", use_container_width=True)
        if st.button('메달 페이지', icon='🏅', type="tertiary", use_container_width=True):
            st.switch_page("pages/medal.py")

st.html('''
<style>
    div[data-testid="stElementToolbar"] {
        visibility: hidden;
    }
</style>
'''
    )
render()