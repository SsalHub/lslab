import streamlit as st
import utils.cooldowncalc as cooldownCalc

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
    widgets['seg'].segmented_control(
        "조회방식 선택", 
        options=options.keys(), 
        format_func=lambda x: options[x],
        selection_mode="single", 
        key = "dialog_seg",
        label_visibility='hidden',
    )
    # 장비 정보 표시
    gear = st.session_state['gear']
    widgets['image'].image(f"{gear['image']}", use_container_width=True)
    widgets['name'].subheader(gear['name'])
    if st.session_state['dialog_seg'] == 0:
        # 육성->쿨타임 조회
        widgets['toggle'].toggle("직접 입력", value=False, key='dialog_toggle')
        if st.session_state['dialog_toggle']:
            grow = widgets['input'].number_input(" ", min_value=0, max_value=300, value=200, placeholder="육성 수치 입력")
            widgets['result'].write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
        else:
            grow = widgets['input'].slider("나의 육성수치 :", 0, 300, 200, 1)
            widgets['result'].write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
    elif st.session_state['dialog_seg'] == 1:
        # 쿨타임->육성 조회
        cooldown = widgets['input'].slider("최소 ~ 최대 쿨타임 :", cooldownCalc.getCooldown(0, gear['cooldown']), cooldownCalc.getCooldown(300, gear['cooldown']), cooldownCalc.getCooldown(0, gear['cooldown']), 0.1)
        widgets['result'].write(f"{cooldown} 쿨타임을 위한 육성치는 {cooldownCalc.getGrow(cooldown, gear['cooldown'])}입니다.")


def render(gear_list):
    st.html('''
<style>
    div[data-testid="stElementToolbar"] {
        visibility: hidden;
    }
</style>
'''
    )
    ### 페이지 중심 요소 배치
    # 검색창
    st.text_input("장비 이름 검색", key='query', placeholder="장비 이름 입력", label_visibility='hidden')
    # 조회방식 선택
    seg_options = {
        "all": "전체",
        "weapon": "무기",
        "armor": "갑옷",
        "helm": "투구",
        "trinket": "망토",
    }
    _1, seg, selbox = st.columns([1, 2, 1])
    seg.segmented_control(
        "부위 선택", 
        options=seg_options.keys(), 
        selection_mode="single", 
        format_func=lambda x:seg_options[x],
        key = "list_seg",
        default="all",
        label_visibility='collapsed',
    )
    sel_options = [
        "가나다순",
        "쿨타임순"
    ]
    selbox.selectbox(
        "조회방식 선택",
        options=sel_options, 
        index=0, 
        key="list_sel",
        label_visibility='collapsed',
    )
    # 장비 목록 필터링
    if st.session_state['list_sel'] == sel_options[0]:
        # 가나다순 정렬
        gears = sorted(gear_list, key=lambda x: x['name'])
    elif st.session_state['list_sel'] == sel_options[1]:
        # 쿨타임순 정렬
        gears = sorted(gear_list, key=lambda x: x['cooldown'])
    else:
        gears = gear_list
    gears = [gear for gear in gears if gear['part'] == st.session_state['list_seg']] if st.session_state['list_seg'] != 'all' else gears
    if 0 < len(st.session_state.get('query')):
        gears = [gear for gear in gears if st.session_state['query'].lower() in gear['name'].lower()]
    # 장비 목록
    list_area = st.container()
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
