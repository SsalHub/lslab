import streamlit as st

def render():
    st.title("LSLAB")
    st.write("LSLAB에서 이용할 기능을 선택하세요.")
    st.divider()

    cols = st.columns([1, 4, 4, 1])
    with cols[1]:
        container = st.container(border=True)
        container.image("images/gear_ico.png", use_container_width=True)
        if container.button('장비 페이지', icon='🗡️', type="tertiary", use_container_width=True):
            st.switch_page("pages/gear.py")
    with cols[2]:
        container = st.container(border=True)
        container.image("images/medal_ico.png", use_container_width=True)
        if container.button('메달 페이지', icon='🏅', type="tertiary", use_container_width=True):
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