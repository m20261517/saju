from flask import Flask, render_template_string, request
import datetime

app = Flask(__name__)

GANS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
ZIS = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
# 일간의 물상 이모지 매핑
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

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        year = request.form.get('year')
        month = request.form.get('month')
        day = request.form.get('day')
        ilgan, ilju = calc_ilju(year, month, day)
        if ilju:
            emoji = GAN_EMOJI.get(ilgan, '')
            result = f"당신의 일주는 <b>{ilju}</b>입니다.<br>일간: <b>{ilgan}</b> {emoji}"
        else:
            result = "입력이 올바르지 않습니다."
    return render_template_string("""
        <h2>사주 일주(干支) & 일간 물상 이모지 계산기</h2>
        <form method="post">
          생년: <input type="number" name="year" required> 년<br>
          월: <input type="number" name="month" required> 월<br>
          일: <input type="number" name="day" required> 일<br>
          <input type="submit" value="계산">
        </form>
        <p>{{result|safe}}</p>
    """, result=result)

if __name__ == '__main__':
    app.run(debug=True)
