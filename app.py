import streamlit as st
import datetime

GANS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
ZIS = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']

GAN_EMOJI = {
    '갑': '🌳',  # 나무
    '을': '🌱',  # 새싹
    '병': '🔥',  # 태양/불
    '정': '💡',  # 촛불/빛
    '무': '⛰',  # 산
    '기': '🌏',  # 땅/흙
    '경': '🗡',  # 칼/금속
    '신': '⚙',  # 톱니/금속
    '임': '💧',  # 물방울
    '계': '🌊',  # 바다/물결
}

REFERENCE_DATE = datetime.date(1900, 1, 1)
REFERENCE_INDEX = 36  # '경자'일

def get_ganji_index(since):
    delta = (since - REFERENCE_DATE).days
    stem_index = (REFERENCE_INDEX + delta) % 10
    branch_index = (REFERENCE_INDEX + delta) % 12
    return stem_index, branch_index

def calc_ilju(year, month, day):
    try:
        birth = datetime.date(int(year), int(month), int(day))
    except Exception:
        return None, None
    stem_idx, branch_idx = get_ganji_index(birth)
    ilgan = GANS[stem_idx]
    ilju = f"{ilgan}{ZIS[branch_idx]}"
    return ilgan, ilju

st.title("사주 일주(干支) & 일간 물상 이모지 계산기")

with st.form("input_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.number_input("생년", min_value=1900, max_value=2100, value=2000, step=1)
    with col2:
        month = st.number_input("월", min_value=1, max_value=12, value=1, step=1)
    with col3:
        day = st.number_input("일", min_value=1, max_value=31, value=1, step=1)
    submitted = st.form_submit_button("계산")

if submitted:
    ilgan, ilju = calc_ilju(year, month, day)
    if ilju:
        emoji = GAN_EMOJI.get(ilgan, '')
        st.success(f"당신의 일주는 **{ilju}** 입니다.  \n일간: **{ilgan}** {emoji}")
    else:
        st.error("입력이 올바르지 않습니다.")
