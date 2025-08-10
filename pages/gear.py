import pandas as pd
import streamlit as st
import json
import utils.cooldowncalc as cooldownCalc
from utils.browserdetect import isMobile
from numpy.random import default_rng as rng


# 버튼 클릭 시 표시되는 장비 정보 대화박스
@st.dialog("장비 쿨타임 정보")
def showInfoDialog():
    gear = st.session_state.gear
    main_container = st.container(horizontal=True, horizontal_alignment="center", gap=None)
    with main_container.container(width=160, horizontal_alignment="center", vertical_alignment="center"):
        st.image(gear["image"], use_container_width=True)
    with main_container.container(width=240, horizontal_alignment="center"):
        seg_options = {
            0: '육성 -> 쿨타임',
            1: '쿨타임 -> 육성', 
        }
        name_container = st.container(horizontal=True, horizontal_alignment="distribute")
        name_container.html(f'<b style="text-align: center; font-">{gear["name"]}</b>')
        toggle = name_container.empty()
        input, result = st.empty(), st.empty()
        st.segmented_control(
            "label", 
            options=seg_options.keys(), 
            format_func=lambda x: seg_options[x],
            selection_mode="single", 
            key = "dialog_seg",
            label_visibility='collapsed',
            width="content"
        )
        if st.session_state.dialog_seg == 0:
            # 육성->쿨타임 조회
            toggle.toggle("직접 입력", value=False, key="dialog_toggle")
            if st.session_state.dialog_toggle:
                grow = input.number_input(" ", min_value=0, max_value=300, value=200, placeholder="육성 수치 입력")
                result.write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
            else:
                grow = input.slider("나의 육성수치 :", 0, 300, 200, 1)
                result.write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
        elif st.session_state['dialog_seg'] == 1:
            # 쿨타임->육성 조회
            cooldown = input.slider("최소 ~ 최대 쿨타임 :", cooldownCalc.getCooldown(0, gear['cooldown']), cooldownCalc.getCooldown(300, gear['cooldown']), cooldownCalc.getCooldown(0, gear['cooldown']), 0.1)
            result.write(f"{cooldown} 쿨타임을 위한 육성치는 {cooldownCalc.getGrow(cooldown, gear['cooldown'])}입니다.")



def render(gear_list):
    st.html('''
<style>
    div[data-testid="stElementToolbar"] {
        visibility: hidden;
    }
</style>
'''
    )
    seg_options = {
        "all": "전체",
        "weapon": "무기",
        "armor": "갑옷",
        "helm": "투구",
        "trinket": "망토",
    }
    sel_options = [
        "가나다순",
        "쿨타임순"
    ]

    st.title("🗡️장비")
    st.write("이용할 기능을 선택하세요.")
    st.divider()
    compare_container = st.container(horizontal_alignment="center").container(border=True, width=1200, horizontal_alignment="center", vertical_alignment="center")
    compare_container.html('<div style="text-align: center; font-size: 50px; font-weight: bold;">쿨타임 비교 결과</div>')
    if "selected" not in st.session_state or not st.session_state.selected:
        compare_container.html(f'<div style="text-align: center;">장비를 선택하면 쿨타임을 비교합니다.</div>')
    else:
        selected_list_container = compare_container.container(border=False, height=100, horizontal=True, vertical_alignment="center", gap=None)
        with selected_list_container.container(width=90):
            st.write('선택된 장비 : ')
        for gear in st.session_state.selected:
            with selected_list_container.container(width=140, horizontal=True, horizontal_alignment="center", vertical_alignment="center", gap=None):
                gearname = gear["name"] if len(gear["name"]) < 7 else gear["name"][:6] + '...'
                st.image(gear["image"], width=30)
                with st.container(border=False, width=110, vertical_alignment="center", gap=None):
                    st.html(f'<span title={gear["name"]}>{gearname}</span>')
        data = { "육성": [], "쿨타임": [], "장비": [] }
        gear_cooldown = {}
        for gear in st.session_state.selected:
            data["육성"].extend(list(range(300)))
            data["쿨타임"].extend([cooldownCalc.getCooldown(i, gear["cooldown"]) for i in range(300)])
            data["장비"].extend([gear["name"]] * 300)
            gear_cooldown[gear["name"]] = gear["cooldown"]
        df = pd.DataFrame(data)
        compare_container.line_chart(df, x="육성", y="쿨타임", color="장비", use_container_width=False, width=800)
        fastest = min(gear_cooldown, key=gear_cooldown.get)
        compare_container.html(f'<div style="text-align: center;"><h2>가장 쿨타임이 빠른 장비는 <span style="color: #ff0000">{fastest}</span>입니다.</h2></div>')
        compare_container.html(f'<div style="text-align: center;">그래프에 마우스를 올려 상세정보를 확인하세요.</div>')
        with compare_container.container(horizontal_alignment="center"):
            if st.button('초기화', type="primary"):
                del st.session_state["selected"]
                st.rerun()

    query_container = st.container(horizontal_alignment="center").container(width=1200, horizontal=True, horizontal_alignment="center", vertical_alignment="center")
    with query_container.container(width=90):
        st.write('🗡️장비 검색')
    query_container.text_input('이름으로 검색', key='query', placeholder="이름으로 검색", label_visibility="collapsed")
    query_container.selectbox(
        label='정렬 기준 선택 :',
        options=sel_options,
        index=0,
        key="list_sel",
        label_visibility='collapsed',
        width=130
    )
    seg_container = st.container(horizontal=True, horizontal_alignment="center")
    seg_container.segmented_control(
        label="부위 선택 :", 
        options=seg_options.keys(), 
        selection_mode="single", 
        format_func=lambda x:seg_options[x],
        key = "list_seg",
        default="all",
        label_visibility="collapsed",
        width="content"
    )
    
    if st.session_state.list_sel == "가나다순":
        gears = sorted(gear_list, key=lambda x: x['name'])
    elif st.session_state.list_sel == "쿨타임순":
        gears = sorted(gear_list, key=lambda x: x['cooldown'])
    else:
        gears = gear_list
    gears = [gear for gear in gears if gear['part'] == st.session_state.list_seg] if st.session_state.list_seg != 'all' else gears
    if 0 < len(st.session_state.get('query')):
        gears = [gear for gear in gears if st.session_state.query.lower() in gear['name'].lower()]
    list_container = st.container(horizontal_alignment="center").container(border=True, width=1200, height=900, horizontal=True, horizontal_alignment="center", vertical_alignment="center")
    for i in range(len(gears)):
        with list_container.container(border=True, width=170, height=270, horizontal_alignment="center", vertical_alignment="center"):
            gearname = gears[i]["name"] if len(gears[i]["name"]) < 7 else gears[i]["name"][:6] + '...'
            st.image(gears[i]["image"], use_container_width=True)
            st.html(f'<div style="text-align: center; font-size: 16px;"><span class="tooltip" title="{gears[i]["name"]}">{gearname}</span></div>',)
            with st.container(horizontal=True, horizontal_alignment="center"):
                if st.button("보기", key=f"_gear_show_{i}", width="stretch"):
                    st.session_state.dialog_seg = 0
                    st.session_state.gear = gears[i]
                    showInfoDialog()
                if "selected" not in st.session_state or gears[i] not in st.session_state.selected:
                    if st.button("선택", key=f"_gear_select_{i}", type="secondary", width="stretch"):
                        if "selected" not in st.session_state:
                            st.session_state.selected = [ gears[i], ]
                            st.rerun()
                        else:
                            if 10 < len(st.session_state.selected):
                                st.toast('선택할 수 있는 장비가 초과되었습니다.')
                            else:
                                st.session_state.selected.append(gears[i])
                                st.rerun()
                else:
                    if st.button("해제", key=f"_gear_remove_{i}", type="primary", width="stretch"):
                        st.session_state.selected.remove(gears[i])
                        st.rerun()

                    


with open('data/gears.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
render(data["gear"])