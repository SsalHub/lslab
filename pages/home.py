import streamlit as st

def render():
    st.title("LSLAB")
    st.write("LSLAB에서 이용할 기능을 선택하세요.")
    st.divider()

    link_container = st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center")
    with link_container.container(border=True, width=220, horizontal_alignment="center", vertical_alignment="center"):
        if st.button('장비 페이지 바로가기', icon='🗡️', type="tertiary", use_container_width=True):
            st.switch_page("pages/gear.py")
    with link_container.container(border=True, width=220, horizontal_alignment="center", vertical_alignment="center"):
        if st.button('메달 페이지 바로가기', icon='🏅', type="tertiary", use_container_width=True):
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
# from utils.browserdetect import isMobile
# isMobile(st.context.headers['User-Agent'])
