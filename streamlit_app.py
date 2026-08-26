import streamlit as st
import random
from datetime import date


# ============================================================
# 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="오늘의 타로",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 스타일
# ============================================================

st.markdown(
    """
    <style>
        @import url(
            'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900'
            '&family=Playfair+Display:wght@600;700&display=swap'
        );

        .stApp {
            background:
                radial-gradient(
                    circle at 50% 0%,
                    rgba(111, 76, 180, 0.25),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #100b1d 0%,
                    #1b1230 50%,
                    #0b0812 100%
                );
            color: #f8f3ff;
        }

        .main-title {
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-size: 3.2rem;
            font-weight: 700;
            color: #f5d88a;
            margin-top: 20px;
            margin-bottom: 5px;
            text-shadow: 0 0 25px rgba(245, 216, 138, 0.25);
        }

        .subtitle {
            text-align: center;
            color: #c9bdd9;
            font-size: 1rem;
            margin-bottom: 30px;
        }

        .date-box {
            text-align: center;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(245,216,138,0.25);
            border-radius: 15px;
            padding: 12px;
            margin-bottom: 25px;
        }

        .tarot-card {
            background:
                linear-gradient(
                    145deg,
                    #2c1a4a,
                    #120c21
                );
            border: 2px solid #d5ae58;
            border-radius: 24px;
            padding: 35px 25px;
            text-align: center;
            box-shadow:
                0 0 30px rgba(213,174,88,0.15),
                inset 0 0 30px rgba(255,255,255,0.03);
            margin: 20px 0 30px 0;
        }

        .card-symbol {
            font-size: 5rem;
            margin-bottom: 10px;
        }

        .card-name {
            font-family: 'Playfair Display', serif;
            font-size: 2rem;
            color: #f5d88a;
            margin-bottom: 8px;
        }

        .card-position {
            color: #c9bdd9;
            font-size: 0.9rem;
        }

        .fortune-box {
            background: rgba(255,255,255,0.055);
            border-left: 4px solid #d5ae58;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
        }

        .fortune-title {
            color: #f5d88a;
            font-weight: 700;
            font-size: 1.05rem;
            margin-bottom: 8px;
        }

        .fortune-text {
            color: #eee7f5;
            line-height: 1.75;
        }

        .keyword {
            display: inline-block;
            background: rgba(213,174,88,0.15);
            border: 1px solid rgba(213,174,88,0.35);
            border-radius: 20px;
            padding: 6px 12px;
            margin: 4px;
            color: #f5d88a;
        }

        .warning {
            background: rgba(160, 90, 90, 0.13);
            border: 1px solid rgba(220,120,120,0.3);
            border-radius: 12px;
            padding: 15px;
            color: #ead1d1;
            line-height: 1.7;
        }

        .footer {
            text-align: center;
            color: #80758d;
            font-size: 0.8rem;
            margin-top: 45px;
            padding-bottom: 20px;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 1px solid #d5ae58;
            background: linear-gradient(
                135deg,
                #6d479f,
                #39215e
            );
            color: white;
            font-size: 1.1rem;
            font-weight: 700;
            padding: 12px;
            transition: 0.2s;
        }

        div.stButton > button:hover {
            border-color: #f5d88a;
            color: #f5d88a;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 타로 카드 데이터
# ============================================================

TAROT_CARDS = [
    {
        "name": "바보 (The Fool)",
        "symbol": "🌟",
        "keywords": ["새로운 시작", "모험", "용기"],
        "general": "오늘은 익숙한 길보다 새로운 길에서 좋은 기회를 발견할 수 있는 날입니다. 완벽한 준비를 기다리기보다 작은 한 걸음을 내딛어 보세요.",
        "love": "연애에서는 예상하지 못했던 만남이나 새로운 분위기가 찾아올 수 있습니다. 솔직한 표현이 관계를 가볍고 즐겁게 만들어 줍니다.",
        "money": "금전적으로 새로운 기회가 보일 수 있지만 충동적인 지출은 조심하세요. 새로운 것을 시작한다면 작은 규모부터 시험하는 것이 좋습니다.",
        "work": "새로운 프로젝트나 아이디어를 시작하기 좋은 날입니다. 기존의 방식에서 벗어난 접근이 좋은 결과를 가져올 수 있습니다.",
        "advice": "두려움 때문에 기회를 놓치지 마세요. 다만 무모함과 용기는 다르다는 점을 기억하세요.",
    },
    {
        "name": "마법사 (The Magician)",
        "symbol": "✨",
        "keywords": ["능력", "집중", "실행력"],
        "general": "오늘 당신에게는 생각한 것을 현실로 옮길 수 있는 힘이 있습니다. 중요한 것은 능력보다 집중력입니다.",
        "love": "당신의 매력이 자연스럽게 드러나는 날입니다. 마음에 두고 있는 사람이 있다면 먼저 대화를 시작해 보세요.",
        "money": "자신이 가진 능력을 활용하면 새로운 수입의 가능성을 발견할 수 있습니다. 아이디어를 실제 행동으로 옮겨보세요.",
        "work": "업무에서 주도권을 잡기에 좋은 날입니다. 자신의 아이디어를 명확하게 설명하면 주변의 도움을 받을 가능성이 높습니다.",
        "advice": "이미 가지고 있는 도구와 능력을 다시 살펴보세요. 생각보다 많은 것을 할 수 있습니다.",
    },
    {
        "name": "여사제 (The High Priestess)",
        "symbol": "🌙",
        "keywords": ["직관", "비밀", "내면"],
        "general": "오늘은 외부의 목소리보다 자신의 직감을 믿어야 하는 날입니다. 서두르지 말고 상황을 관찰하세요.",
        "love": "상대방의 말보다 행동에 주목하세요. 아직 드러나지 않은 감정이 있을 수 있습니다.",
        "money": "확실하지 않은 투자나 계약은 잠시 기다리는 편이 좋습니다. 정보를 충분히 확인한 뒤 결정하세요.",
        "work": "눈에 보이는 정보만으로 판단하지 마세요. 동료의 의도나 상황의 흐름을 관찰하면 중요한 힌트를 얻을 수 있습니다.",
        "advice": "모든 답을 지금 당장 알 필요는 없습니다. 기다림 자체가 답을 가져다줄 때가 있습니다.",
    },
    {
        "name": "여제 (The Empress)",
        "symbol": "🌺",
        "keywords": ["풍요", "사랑", "성장"],
        "general": "오늘은 풍요와 성장의 에너지가 강한 날입니다. 자신과 주변 사람을 돌보는 행동이 좋은 흐름을 만들어 줍니다.",
        "love": "따뜻한 감정이 깊어질 수 있습니다. 연인이 있다면 함께 편안한 시간을 보내세요.",
        "money": "금전적으로 안정적인 흐름이 예상됩니다. 장기적으로 가치가 있는 것에 투자하는 것을 고려해 볼 수 있습니다.",
        "work": "창의적인 아이디어가 빛나는 날입니다. 특히 디자인, 콘텐츠, 기획과 관련된 일에서 좋은 결과가 있을 수 있습니다.",
        "advice": "결과만 재촉하지 말고 성장하는 과정을 즐겨보세요.",
    },
    {
        "name": "황제 (The Emperor)",
        "symbol": "👑",
        "keywords": ["질서", "책임", "리더십"],
        "general": "오늘은 감정보다 현실적인 판단이 중요한 날입니다. 계획을 세우고 순서대로 실행하면 안정적인 결과를 얻을 수 있습니다.",
        "love": "관계에서 책임감과 신뢰가 중요해집니다. 상대방에게 확실한 태도를 보여주세요.",
        "money": "재정 계획을 점검하기 좋은 날입니다. 예산을 정하고 불필요한 지출을 줄이면 안정성이 높아집니다.",
        "work": "리더십을 발휘할 기회가 생길 수 있습니다. 책임을 피하지 말고 주도적으로 움직여 보세요.",
        "advice": "통제할 수 있는 것과 통제할 수 없는 것을 구분하세요.",
    },
    {
        "name": "연인 (The Lovers)",
        "symbol": "💕",
        "keywords": ["사랑", "선택", "조화"],
        "general": "오늘은 사람과의 관계가 중요한 역할을 하는 날입니다. 중요한 선택을 앞두고 있다면 자신의 진짜 마음을 살펴보세요.",
        "love": "연애운이 매우 좋은 카드입니다. 솔직한 대화와 진심 어린 표현이 관계를 한 단계 발전시킬 수 있습니다.",
        "money": "혼자 결정하기보다 믿을 수 있는 사람과 의견을 나누면 좋은 선택을 할 수 있습니다.",
        "work": "협업과 파트너십에서 좋은 결과가 예상됩니다. 혼자 모든 것을 해결하려 하지 마세요.",
        "advice": "남이 원하는 선택이 아니라 자신이 진정으로 원하는 선택을 하세요.",
    },
    {
        "name": "전차 (The Chariot)",
        "symbol": "🏆",
        "keywords": ["승리", "추진력", "목표"],
        "general": "목표를 향해 강하게 전진할 수 있는 날입니다. 주변의 방해에 흔들리지 말고 방향을 유지하세요.",
        "love": "관계에서 적극적인 행동이 좋은 결과를 가져올 수 있습니다. 마음을 표현하는 것을 두려워하지 마세요.",
        "money": "목표를 명확히 하면 재정적인 성과를 만들 수 있습니다. 계획한 일을 미루지 마세요.",
        "work": "경쟁에서 앞서갈 수 있는 날입니다. 중요한 업무부터 빠르게 처리하세요.",
        "advice": "속도도 중요하지만 방향이 더 중요합니다.",
    },
    {
        "name": "힘 (Strength)",
        "symbol": "🦁",
        "keywords": ["인내", "자신감", "내면의 힘"],
        "general": "오늘의 힘은 강하게 밀어붙이는 것이 아니라 차분하게 버티는 데서 나옵니다.",
        "love": "감정적인 상황에서도 부드러운 태도를 유지하면 관계가 더욱 깊어집니다.",
        "money": "단기적인 욕심보다 꾸준한 관리가 중요합니다. 작은 절약이 큰 차이를 만들 수 있습니다.",
        "work": "어려운 업무도 포기하지 않고 꾸준히 진행하면 결국 좋은 결과를 얻을 수 있습니다.",
        "advice": "당신이 생각하는 것보다 훨씬 강한 사람입니다. 조급해하지 마세요.",
    },
    {
        "name": "은둔자 (The Hermit)",
        "symbol": "🏮",
        "keywords": ["성찰", "지혜", "혼자만의 시간"],
        "general": "오늘은 다른 사람의 의견보다 자신의 생각을 정리하는 시간이 필요합니다.",
        "love": "잠시 혼자만의 시간이 필요할 수 있습니다. 거리를 두는 것이 반드시 관계의 끝을 의미하지는 않습니다.",
        "money": "큰 결정을 내리기 전에 충분히 조사하세요. 전문가의 의견을 참고하는 것도 좋습니다.",
        "work": "집중력이 높아지는 날입니다. 혼자 처리해야 하는 업무를 먼저 해결해 보세요.",
        "advice": "답은 밖에만 있는 것이 아닙니다. 잠시 조용히 자신을 바라보세요.",
    },
    {
        "name": "운명의 수레바퀴 (Wheel of Fortune)",
        "symbol": "🎡",
        "keywords": ["변화", "행운", "전환점"],
        "general": "오늘은 예상하지 못했던 변화가 찾아올 수 있습니다. 흐름이 바뀌는 순간을 놓치지 마세요.",
        "love": "뜻밖의 만남이나 연락이 들어올 가능성이 있습니다. 과거의 인연이 다시 등장할 수도 있습니다.",
        "money": "금전적인 흐름에 변화가 생길 수 있습니다. 좋은 기회가 오면 너무 오래 고민하지 마세요.",
        "work": "업무 환경이나 계획에 변화가 생길 수 있습니다. 변화에 유연하게 대응하면 오히려 기회가 됩니다.",
        "advice": "모든 것을 통제하려 하지 말고 변화의 흐름을 활용하세요.",
    },
    {
        "name": "정의 (Justice)",
        "symbol": "⚖️",
        "keywords": ["균형", "공정함", "결정"],
        "general": "오늘은 감정적인 판단보다 사실과 균형을 기준으로 생각해야 하는 날입니다.",
        "love": "서로의 입장을 솔직하게 이야기하면 오해를 풀 수 있습니다.",
        "money": "계약이나 금전 거래가 있다면 작은 글씨까지 꼼꼼히 확인하세요.",
        "work": "공정한 평가를 받을 가능성이 있습니다. 자신의 성과를 객관적인 자료로 정리해 두세요.",
        "advice": "당신의 선택에는 책임이 따릅니다. 하지만 공정하게 판단한다면 후회가 적을 것입니다.",
    },
    {
        "name": "별 (The Star)",
        "symbol": "⭐",
        "keywords": ["희망", "회복", "긍정"],
        "general": "오늘은 희망적인 에너지가 강합니다. 지금 당장 결과가 보이지 않아도 좋은 방향으로 움직이고 있습니다.",
        "love": "따뜻하고 긍정적인 관계의 흐름이 들어옵니다. 솔직한 마음을 표현해 보세요.",
        "money": "장기적인 계획에 희망적인 신호가 나타날 수 있습니다. 꾸준함을 유지하세요.",
        "work": "창의성과 영감이 살아나는 날입니다. 새로운 아이디어를 기록해 두세요.",
        "advice": "아직 보이지 않는 미래를 믿어보세요.",
    },
    {
        "name": "태양 (The Sun)",
        "symbol": "☀️",
        "keywords": ["성공", "기쁨", "긍정"],
        "general": "오늘은 매우 밝고 긍정적인 카드입니다. 자신감을 가지고 행동할수록 좋은 결과가 따라올 가능성이 높습니다.",
        "love": "즐겁고 따뜻한 관계의 흐름입니다. 싱글이라면 밝은 분위기의 만남을 기대해 볼 수 있습니다.",
        "money": "노력에 대한 보상이나 좋은 소식이 있을 수 있습니다.",
        "work": "성과가 눈에 띄는 날입니다. 자신이 해온 일을 당당하게 보여주세요.",
        "advice": "오늘은 지나치게 의심하기보다 좋은 것을 있는 그대로 즐겨보세요.",
    },
    {
        "name": "세계 (The World)",
        "symbol": "🌍",
        "keywords": ["완성", "성취", "새로운 단계"],
        "general": "하나의 사이클이 완성되고 새로운 단계로 넘어가는 시기입니다. 그동안의 노력을 인정해주세요.",
        "love": "관계가 한 단계 깊어질 수 있습니다. 오래된 관계에서는 중요한 결실이 나타날 수 있습니다.",
        "money": "장기간 노력한 일이 성과로 연결될 가능성이 있습니다.",
        "work": "프로젝트의 마무리나 중요한 목표 달성에 좋은 흐름입니다.",
        "advice": "지금까지 걸어온 길을 돌아보고 스스로의 성취를 인정하세요.",
    },
]


# ============================================================
# 운세 점수
# ============================================================

def make_score(seed_value: int, offset: int = 0) -> int:
    """오늘 날짜와 카드 정보를 바탕으로 60~99 사이 점수를 만든다."""
    rng = random.Random(seed_value + offset)
    return rng.randint(60, 99)


def get_today_card():
    """오늘 날짜를 기준으로 카드가 매일 일정하게 선택되도록 한다."""
    today = date.today()

    seed = (
        today.year * 10000
        + today.month * 100
        + today.day
    )

    rng = random.Random(seed)

    return rng.choice(TAROT_CARDS), seed


# ============================================================
# 세션 상태
# ============================================================

if "drawn" not in st.session_state:
    st.session_state.drawn = False

if "card" not in st.session_state:
    st.session_state.card = None

if "seed" not in st.session_state:
    st.session_state.seed = None


# ============================================================
# 화면 상단
# ============================================================

st.markdown(
    '<div class="main-title">🔮 오늘의 타로</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    '오늘 하루를 위한 한 장의 타로 메시지'
    '</div>',
    unsafe_allow_html=True,
)

today = date.today()

st.markdown(
    f"""
    <div class="date-box">
        ✨ 오늘은 <b>{today.strftime("%Y년 %m월 %d일")}</b>입니다.<br>
        당신에게 필요한 메시지를 확인해 보세요.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 사용자 입력
# ============================================================

name = st.text_input(
    "이름 또는 닉네임",
    placeholder="예: 홍길동",
)

category = st.selectbox(
    "오늘 가장 궁금한 분야",
    [
        "전체운",
        "연애운",
        "금전운",
        "직장·사업운",
    ],
)


# ============================================================
# 카드 뽑기
# ============================================================

if st.button("🔮 오늘의 타로 카드 뽑기"):

    card, seed = get_today_card()

    st.session_state.card = card
    st.session_state.seed = seed
    st.session_state.drawn = True


# ============================================================
# 결과
# ============================================================

if st.session_state.drawn:

    card = st.session_state.card
    seed = st.session_state.seed

    st.markdown(
        f"""
        <div class="tarot-card">

            <div class="card-symbol">
                {card["symbol"]}
            </div>

            <div class="card-name">
                {card["name"]}
            </div>

            <div class="card-position">
                오늘의 카드
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if name.strip():
        st.markdown(
            f"### ✨ {name.strip()}님을 위한 오늘의 메시지"
        )
    else:
        st.markdown("### ✨ 당신을 위한 오늘의 메시지")

    # --------------------------------------------------------
    # 키워드
    # --------------------------------------------------------

    keywords_html = ""

    for keyword in card["keywords"]:
        keywords_html += (
            f'<span class="keyword">{keyword}</span>'
        )

    st.markdown(
        keywords_html,
        unsafe_allow_html=True,
    )

    st.write("")

    # --------------------------------------------------------
    # 분야별 운세
    # --------------------------------------------------------

    if category == "전체운":
        fortune = card["general"]

    elif category == "연애운":
        fortune = card["love"]

    elif category == "금전운":
        fortune = card["money"]

    else:
        fortune = card["work"]

    st.markdown(
        f"""
        <div class="fortune-box">

            <div class="fortune-title">
                🔮 오늘의 {category}
            </div>

            <div class="fortune-text">
                {fortune}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # 오늘의 점수
    # --------------------------------------------------------

    st.markdown("### 📊 오늘의 운세 점수")

    if category == "전체운":
        offset = 1
    elif category == "연애운":
        offset = 2
    elif category == "금전운":
        offset = 3
    else:
        offset = 4

    score = make_score(
        seed,
        offset=offset,
    )

    st.progress(score / 100)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:1.8rem;
            font-weight:700;
            color:#f5d88a;
            margin-top:10px;
            margin-bottom:20px;
        ">
            {score} / 100
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # 오늘의 조언
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="fortune-box">

            <div class="fortune-title">
                🌙 오늘의 조언
            </div>

            <div class="fortune-text">
                {card["advice"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # 주의사항
    # --------------------------------------------------------

    st.markdown("### ⚠️ 오늘 기억할 것")

    st.markdown(
        """
        <div class="warning">
        타로는 미래를 확정적으로 예측하는 도구가 아니라,
        오늘 하루를 돌아보고 자신의 생각을 정리하기 위한
        재미와 자기성찰의 콘텐츠입니다.
        중요한 금전·건강·법률 등의 결정은 타로 결과만으로
        판단하지 마세요.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 하단
# ============================================================

st.markdown(
    """
    <div class="footer">
        🔮 오늘의 타로 · Daily Tarot<br>
        재미와 자기성찰을 위한 운세 콘텐츠
    </div>
    """,
    unsafe_allow_html=True,
)
