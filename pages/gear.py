import streamlit as st
from PIL import Image
import utils.cooldowncalc as cooldownCalc
import json

# 버튼 클릭 시 표시되는 장비 정보 대화박스
@st.dialog("장비 쿨타임 정보")
def showInfoDialog():
    leftside, rightside = st.columns([1, 2])
    right_top = rightside.columns(2)
    widgets = {
        'image': leftside.empty(),
        'name': right_top[0].empty(),
        'toggle': right_top[1].empty(),
        'input': rightside.empty(),
        'result': rightside.empty(),
        'seg': rightside.empty(),
    }

    # 장비 정보 조회방식 선택
    options = {
        0: '육성 -> 쿨타임',
        1: '쿨타임 -> 육성', 
    }
    widgets['seg'].empty().segmented_control(
        "조회방식 선택", 
        options=options.keys(), 
        format_func=lambda x: options[x],
        selection_mode="single", 
        key = "dialog_seg",
        label_visibility='hidden',
    )
    # 장비 정보 표시
    gear = st.session_state['gear']
    widgets['image'].empty().image(f"{gear['image']}", use_container_width=True)
    widgets['name'].empty().subheader(gear['name'])
    if st.session_state['dialog_seg'] == 0:
        # 육성->쿨타임 조회
        widgets['toggle'].empty().toggle("직접 입력", value=False, key='dialog_toggle')
        if st.session_state['dialog_toggle']:
            grow = widgets['input'].empty().number_input(" ", min_value=0, max_value=300, value=200, placeholder="육성 수치 입력", label_visibility='hidden')
            widgets['result'].empty().write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
        else:
            grow = widgets['input'].empty().slider("나의 육성수치 :", 0, 300, 200, 1)
            widgets['result'].empty().write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
    elif st.session_state['dialog_seg'] == 1:
        # 쿨타임->육성 조회
        cooldown = widgets['input'].empty().slider("최소 ~ 최대 쿨타임 :", cooldownCalc.getCooldown(0, gear['cooldown']), cooldownCalc.getCooldown(300, gear['cooldown']), cooldownCalc.getCooldown(0, gear['cooldown']), 0.1)
        widgets['result'].empty().write(f"{cooldown} 쿨타임을 위한 육성치는 {cooldownCalc.getGrow(cooldown, gear['cooldown'])}입니다.")




def render():
    ### 페이지 중심 요소 배치
    # 타이틀 및 기본 요소 표시
    st.page_link("pages/home.py", label="⬅ 홈으로 돌아가기", icon="🏠")
    st.title("장비")
    st.write("쿨타임 정보를 검색하고 확인하세요.")

    # 메인 컨테이너
    maincontent = st.container()
    # 검색창
    search_query = maincontent.text_input("장비 이름 검색", placeholder="장비 이름 입력", label_visibility='hidden')
    # 장비 목록
    list_area = maincontent.container()
    rows = []
    col_max = 4
    for row_in_step in range(0, len(gears), col_max):
        rows.append(list_area.columns(col_max))
        row = row_in_step // col_max
        col_len = col_max if row_in_step + col_max <= len(gears) else len(gears) - row_in_step
        for j in range(0, col_len):
            with rows[row][j]:
                with st.container(border=True):
                    st.image(gears[col_max * row + j]['image'], use_container_width=True)
                    st.html(f"<div style=\"text-align: center; margin-bottom: 10px;\">{gears[col_max * row + j]['name']}</div>",)
                    if st.button("선택", key=f"gear_{col_max * row + j}", use_container_width=True):
                        st.session_state['dialog_seg'] = 0
                        st.session_state['gear'] = gears[col_max * row + j]
                        showInfoDialog()

### 페이지 설정
# 필요한 파일 로드
with open('data/gears.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 페이지 설정
st.set_page_config(page_title="장비 페이지")
# 장비 데이터 정렬
gears = sorted(data['gear'], key=lambda x: x['name'])
# 페이지 렌더링
render()