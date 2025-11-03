import streamlit as st

st.set_page_config(page_title="🌈 MBTI 책 & 영화 추천", page_icon="📚", layout="centered")

st.title("🌈 MBTI별 책 & 영화 추천 🎬")
st.write("안녕! 👋 너의 MBTI를 선택하면 너한테 어울리는 **책 2권📖**과 **영화 2편🎥**을 추천해줄게!")

# MBTI 목록
mbti_list = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("👉 너의 MBTI를 골라봐!", mbti_list)

# 데이터 (간단 예시)
recommendations = {
    "INTJ": {
        "books": ["📘 생각의 탄생 – 루트번스타인", "📗 이기적 유전자 – 리처드 도킨스"],
        "movies": ["🎬 인터스텔라", "🎥 인셉션"]
    },
    "INFP": {
        "books": ["📙 작은 아씨들 – 루이자 메이 올컷", "📕 연을 쫓는 아이 – 카를레드 호세이니"],
        "movies": ["🎬 월-E", "🎥 어바웃 타임"]
    },
    "ENFP": {
        "books": ["📘 무지개를 건너는 사람 – 모리 히로시", "📗 불편한 편의점 – 김호연"],
        "movies": ["🎬 인사이드 아웃", "🎥 라라랜드"]
    },
    "ISTJ": {
        "books": ["📙 나미야 잡화점의 기적 – 히가시노 게이고", "📕 7년의 밤 – 정유정"],
        "movies": ["🎬 더 킹", "🎥 조커"]
    },
    "ESFP": {
        "books": ["📘 아주 작은 습관의 힘 – 제임스 클리어", "📗 트렌드 코리아 2025 – 김난도"],
        "movies": ["🎬 위대한 쇼맨", "🎥 인턴"]
    },
}

# 기본값 처리
if mbti not in recommendations:
    st.warning("🧐 아직 이 MBTI는 준비 중이야! 곧 추가될 예정이야 💫")
else:
    rec = recommendations[mbti]

    st.subheader(f"🌟 {mbti} 타입에게 딱 어울리는 추천 리스트!")
    st.write("💫 **추천 도서**")
    for b in rec["books"]:
        st.write(f"• {b}")

    st.write("🎬 **추천 영화**")
    for m in rec["movies"]:
        st.write(f"• {m}")

st.markdown("---")
st.info("🌈 너의 성격에 맞는 콘텐츠로 세상을 넓혀봐! 다음엔 게임이나 진로 추천도 추가할까? 😄")
