import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(
    page_title="신비한 타로 점술소 Professional - 7장 종합운세",
    page_icon="🔮",
    layout="wide"
)

# 커스텀 CSS로 프리미엄 분위기 조성
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');
    
    html, body, [data-testid="stStandardExecutionContext"] {
        font-family: 'Noto+Serif+KR', serif;
    }

    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    .tarot-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .tarot-card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.05) 0%, transparent 70%);
        pointer-events: none;
    }

    .tarot-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.2);
        border-color: #f1c40f;
    }
    
    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 15px;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));
    }
    
    .card-title {
        color: #d4af37;
        font-size: 1.4rem;
        margin-bottom: 10px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    .card-meaning {
        font-size: 0.9rem;
        color: #cfd8dc;
        line-height: 1.6;
        text-align: justify;
        word-break: keep-all;
    }
    
    .spread-label {
        color: #9b59b6;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-size: 1.1rem;
        text-align: center;
        border-bottom: 1px solid #9b59b6;
        display: inline-block;
        width: 100%;
    }
    
    .mystical-header {
        text-align: center;
        padding: 40px 0;
        background: linear-gradient(to right, #d4af37, #f1c40f, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    .analysis-box {
        background: rgba(44, 62, 80, 0.4);
        border-left: 5px solid #d4af37;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 타로 카드 데이터
TAROT_DECK = {
    "0. 광대 (The Fool)": {"icon": "🎭", "meaning": "새로운 시작, 자유, 모험. 과거의 굴레에서 벗어나 미지의 세계로 발걸음을 내딛을 때입니다."},
    "1. 마법사 (The Magician)": {"icon": "🪄", "meaning": "창조성, 능력, 자신감. 당신은 이미 목적을 달성하기 위한 모든 자원과 능력을 갖추고 있습니다."},
    "2. 고위 여사제 (The High Priestess)": {"icon": "📖", "meaning": "직관, 지혜, 내면의 소리. 고요히 사색하며 지식을 쌓고 타이밍을 기다리는 것이 현명합니다."},
    "3. 여황제 (The Empress)": {"icon": "👑", "meaning": "풍요, 결실, 모성애. 삶의 모든 영역에서 풍요로움과 창조적인 활력이 샘솟는 시기입니다."},
    "4. 황제 (The Emperor)": {"icon": "🏛️", "meaning": "권위, 구조, 안정. 이성적이고 논리적인 판단으로 상황을 통제하고 책임감을 보여주세요."},
    "5. 교황 (The Hierophant)": {"icon": "⛪", "meaning": "전통, 교육, 멘토. 정해진 절차와 형식을 따르는 것이 지금의 혼란을 정리해 줄 것입니다."},
    "6. 연인 (The Lovers)": {"icon": "💖", "meaning": "조화, 선택, 사랑. 서로를 존중하고 이해하는 태도가 모든 관계의 어려움을 해결하는 열쇠가 됩니다."},
    "7. 전차 (The Chariot)": {"icon": "🛡️", "meaning": "의지, 승리, 돌파. 강한 의지력과 결단력으로 앞에 놓인 장애물을 정면으로 돌파하세요."},
    "8. 힘 (Strength)": {"icon": "🦁", "meaning": "인내, 부드러운 통제. 육체적인 강인함보다 내면의 인내와 부드러운 통제력이 빛을 발할 때입니다."},
    "9. 은둔자 (The Hermit)": {"icon": " Lantern", "meaning": "성찰, 지혜, 고독. 외부의 소음에서 벗어나 스스로의 내면을 깊이 성찰해야 하는 시간입니다."},
    "10. 운명의 수레바퀴 (Wheel of Fortune)": {"icon": "🎡", "meaning": "변화, 행운, 순환. 피할 수 없는 행운이나 전환점이 찾아왔으니 변화의 흐름을 타세요."},
    "11. 정의 (Justice)": {"icon": "⚖️", "meaning": "공정, 균형, 인과응보. 객관적인 사실에 입각하여 모든 상황을 공정하게 판단해야 합니다."},
    "12. 매달린 사람 (The Hanged Man)": {"icon": "🧗", "meaning": "희생, 새로운 관점. 기존의 사고방식을 뒤집어 전혀 새로운 관점에서 바라보는 역발상이 필요합니다."},
    "13. 죽음 (Death)": {"icon": "⌛", "meaning": "종결, 변화, 새로운 시작. 낡은 습관이나 관계가 완전히 끝을 맺고 새로운 가능성이 열리는 시기입니다."},
    "14. 절제 (Temperance)": {"icon": "🏺", "meaning": "조화, 중용, 융합. 서로 다른 요소들을 평화롭게 융합하고 중용의 도를 지켜야 할 때입니다."},
    "15. 악마 (The Devil)": {"icon": "👹", "meaning": "속박, 중독, 물질적 집착. 중독적인 습관이나 물질적인 집착에서 벗어나려는 자유 의지가 필요합니다."},
    "16. 탑 (The Tower)": {"icon": "⚡", "meaning": "격변, 붕괴, 깨달음. 갑작스러운 변화가 닥쳐올 수 있으나 이는 허상을 무너뜨리고 진실을 드러내는 과정입니다."},
    "17. 별 (The Star)": {"icon": "✨", "meaning": "희망, 영감, 치유. 고난을 지나 비로소 평화와 희망의 빛을 맞이하게 되는 치유의 시기입니다."},
    "18. 달 (The Moon)": {"icon": "🌙", "meaning": "불확실성, 불안, 환상. 막막함 속에 직관의 힘이 절실히 필요하며 무의식의 목소리에 귀를 기울이세요."},
    "19. 태양 (The Sun)": {"icon": "☀️", "meaning": "성공, 기쁨, 활력. 인생에서 가장 환하고 눈부신 성공과 기쁨의 에너지가 당신을 감싸고 있습니다."},
    "20. 심판 (Judgement)": {"icon": "🎺", "meaning": "부활, 소명, 결단. 지나온 삶에 대한 결산을 하고 새로운 소명을 향해 다시 태어나는 때입니다."},
    "21. 세계 (The World)": {"icon": "🌍", "meaning": "완성, 성취, 통합. 하나의 큰 주기가 완벽하게 마무리되고 최상의 조화와 승리를 거머쥐게 됩니다."}
}

def draw_cards():
    return random.sample(list(TAROT_DECK.items()), 7)

# 메인 UI
st.markdown('<div class="mystical-header">7장 종합운세 점술소</div>', unsafe_allow_html=True)

if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = None
    st.session_state.flipped = [False] * 7

with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("### 당신의 삶을 관통하는 7가지 운명을 확인하세요.")
        st.write("현재, 과거, 미래부터 당신의 내면과 외부 환경, 조언과 최종 결과까지 심층 분석해 드립니다.")
        if st.button("✨ 7장의 운명 카드 섞기 & 뽑기", use_container_width=True):
            with st.status("신비로운 에너지를 모으는 중...", expanded=False) as status:
                time.sleep(1.5)
                status.update(label="셔플 완료!", state="complete")
            
            st.session_state.drawn_cards = draw_cards()
            st.session_state.flipped = [False] * 7
            st.balloons()

if st.session_state.drawn_cards:
    st.write("---")
    
    labels = [
        "1. 현재 (Current)", "2. 과거 (Past)", "3. 미래 (Future)", 
        "4. 내면 (Inner)", "5. 외부 (Outer)", "6. 조언 (Advice)", "7. 결과 (Result)"
    ]
    
    meaning_points = [
        "지금의 핵심 상황과 감정 상태", "현재에 영향을 준 원인/과거 사건", "흐름이 이어지면 나타날 가능성",
        "본인 내면의 생각·감정·욕망", "주변 환경·사람의 영향·외부 요인", "지금 해야 할 행동/마음가짐", "최종 흐름과 결말(가능성)"
    ]

    # 4 + 3 레이아웃
    row1 = st.columns(4)
    row2 = st.columns(3)
    
    all_slots = row1 + row2
    
    for i, (card_name, data) in enumerate(st.session_state.drawn_cards):
        with all_slots[i]:
            st.markdown(f'<div class="spread-label">{labels[i]}</div>', unsafe_allow_html=True)
            st.caption(meaning_points[i])
            
            card_placeholder = st.empty()
            
            if not st.session_state.flipped[i]:
                with card_placeholder.container():
                    st.markdown("""
                    <div class="tarot-card">
                        <div style="font-size: 4rem; color: #d4af37; margin-bottom: 15px;">🌙</div>
                        <p style="font-size: 1rem; color: #d4af37; font-weight: bold;">봉인된 카드</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"해제", key=f"btn_{i}", use_container_width=True):
                        st.session_state.flipped[i] = True
                        st.rerun()
            else:
                with card_placeholder.container():
                    st.markdown(f"""
                    <div class="tarot-card">
                        <div class="card-icon">{data['icon']}</div>
                        <div class="card-title">{card_name}</div>
                        <div class="card-meaning">{data['meaning']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    if all(st.session_state.flipped):
        st.write("---")
        st.subheader("🔮 7장 종합 운세 실타래 분석")
        
        cards = st.session_state.drawn_cards
        
        analysis_text = f"""
        당신은 현재 **{cards[0][0]}**의 기운 아래 서 있으며, 이는 과거의 **{cards[1][0]}** 사건으로부터 기인한 흐름입니다. 
        이대로 나아간다면 **{cards[2][0]}**의 미래를 맞이할 가능성이 높습니다. 
        
        당신의 진정한 속마음은 **{cards[3][0]}**를 향하고 있지만, 외부 환경인 **{cards[4][0]}**가 당신에게 큰 변수로 작용하고 있습니다. 
        운명은 당신에게 **{cards[5][0]}**의 태도를 가질 것을 조언하고 있으며, 이를 가슴에 새긴다면 최종적으로 **{cards[6][0]}**의 결실을 맺게 될 것입니다.
        """

        st.markdown(f"""
        <div class="analysis-box">
            <p style="font-size: 1.1rem; line-height: 1.8; color: #ffffff; white-space: pre-line;">
                {analysis_text}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 새로운 운명 점치기", use_container_width=True):
            st.session_state.drawn_cards = None
            st.session_state.flipped = [False] * 7
            st.rerun()

# 푸터
st.markdown("""
<div style="text-align: center; margin-top: 60px; color: #444; font-size: 0.85rem; border-top: 1px solid #333; padding-top: 20px;">
    © 2026 Mystical Tarot Lab Professional | Comprehensive 7-Card Spread<br>
    <i>"Astra regunt homines, sed regit astra Deus"</i>
</div>
""", unsafe_allow_html=True)
