import streamlit as st
from PIL import Image
import utils.cooldowncalc as cooldownCalc
import json

# 버튼 클릭 시 표시되는 장비 정보 대화박스
@st.dialog("장비 쿨타임 정보")
def showInfoDialog(gear):
    leftside, rightside = st.columns([1, 2])
    gearinfo = {
        'image': leftside.empty(),
        'name': rightside.empty(),
        'slider': rightside.empty(),
        'result': rightside.empty(),
        'seg': rightside.empty(),
    }
    # 장비 정보 조회방식 선택
    options = {
        0: '육성 -> 쿨타임',
        1: '쿨타임 -> 육성', 
    }
    seg = gearinfo['seg'].empty().segmented_control(
        "", 
        options=options.keys(), 
        format_func=lambda x: options[x],
        selection_mode="single", 
        default=0
    )
    # 장비 정보 표시
    if seg == 0:
        gearinfo['image'].empty().image(f"{gear['image']}", use_container_width=True)
        gearinfo['name'].empty().subheader(gear['name'])
        grow = gearinfo['slider'].empty().slider("나의 육성수치 :", 0, 300, 200, 1)
        gearinfo['result'].empty().write(f"육성 {grow}에서의 쿨타임은 {cooldownCalc.getCooldown(grow, gear['cooldown'])}입니다.")
    else:
        gearinfo['image'].empty().image(f"{gear['image']}", use_container_width=True)
        gearinfo['name'].empty().subheader(gear['name'])
        cooldown = gearinfo['slider'].empty().slider("최소 ~ 최대 쿨타임 :", cooldownCalc.getCooldown(0, gear['cooldown']), cooldownCalc.getCooldown(300, gear['cooldown']), cooldownCalc.getCooldown(0, gear['cooldown']), 0.1)
        gearinfo['result'].empty().write(f"{cooldown} 쿨타임을 위한 육성치는 {cooldownCalc.getGrow(cooldown, gear['cooldown'])}입니다.")


### 페이지 설정
# 필요한 파일 로드
with open('data/gears.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# 페이지 설정
st.set_page_config(
    page_title="장비 페이지",
    page_icon=Image.open("images/ico.png"),
    layout="centered"
)
# 장비 데이터 정렬
gears = sorted(data['gear'], key=lambda x: x['name'])


### 페이지 중심 요소 배치
# 타이틀 및 기본 요소 표시
st.page_link("app.py", label="⬅ 홈으로 돌아가기", icon="🏠")
st.title("장비")
st.write("쿨타임 정보를 검색하고 확인하세요.")

# 메인 컨테이너
maincontent = st.container()
# 검색창
search_query = maincontent.text_input("", placeholder="장비 이름 입력")
# 장비 목록
list_area = maincontent.container()
rows = []
row_len = 4
cols = list_area.columns([row_len, len(gears) / row_len])
for i in range(0, len(gears), row_len):
    rows.append(st.columns(row_len))
    col_len = (len(gears) - 1 - i) % row_len + 1
    for j in range(0, col_len):
        with rows[i][j]:
            with st.container(height=240, border=True):
                st.image(gears[row_len * i + j]['image'], caption=f"{gears[row_len * i + j]['name']}", width=120)
                if st.button("선택", key=f"gear_{row_len * i + j}", use_container_width=True):
                    showInfoDialog(gears[row_len * i + j])
