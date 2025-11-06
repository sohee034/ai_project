# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import Popup, IFrame

st.set_page_config(page_title="Seoul Top10 (for foreigners)", layout="wide")

st.title("🌈 Seoul Top 10 Tourist Spots — 외국인 인기 명소")
st.markdown(
    "Folium으로 서울의 외국인 인기 관광지 Top10을 지도에 표시합니다. 마커를 클릭하면 간단 설명과 링크가 나와요! 😊"
)

# 중심 좌표: 서울 시청 근처
seoul_center = [37.5665, 126.9780]

# Top10 장소 (이름, 위도, 경도, 짧은 설명, 더보기 링크)
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.5796, "lon": 126.9770,
        "desc": "조선의 대표 궁궐. 한복 체험과 수문장 교대식으로 유명.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Changdeokgung Palace (창덕궁)",
        "lat": 37.5789, "lon": 126.9910,
        "desc": "비원(후원)으로 유명한 궁궐. 유네스코 세계유산.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.5826, "lon": 126.9830,
        "desc": "전통 한옥들이 모여있는 골목길. 사진 스팟이 많음.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.5740, "lon": 126.9860,
        "desc": "전통 공예품, 찻집, 기념품 쇼핑에 좋은 거리.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Myeongdong (명동)",
        "lat": 37.5609, "lon": 126.9853,
        "desc": "쇼핑과 길거리 음식의 메카. 화장품 쇼핑 인기 지역.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "N Seoul Tower / Namsan (N서울타워 / 남산)",
        "lat": 37.5512, "lon": 126.9882,
        "desc": "서울 전망 명소. 야경과 '자물쇠' 포인트로 인기.",
        "link": "https://en.wikipedia.org/wiki/N_Seoul_Tower"
    },
    {
        "name": "Hongdae (홍대/홍익대 주변)",
        "lat": 37.5551, "lon": 126.9237,
        "desc": "젊음의 거리, 클럽·카페·스트리트 퍼포먼스 활발.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Dongdaemun Design Plaza (DDP, 동대문 디자인플라자)",
        "lat": 37.5663, "lon": 127.0090,
        "desc": "미래적 건축물과 야간시장, 패션몰이 모여있는 곳.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Gwangjang Market (광장시장)",
        "lat": 37.5704, "lon": 126.9970,
        "desc": "한국 전통 길거리 음식(비빔밥, 빈대떡 등)으로 유명한 재래시장.",
        "link": "https://english.visitkorea.or.kr"
    },
    {
        "name": "Lotte World Tower & Mall (롯데월드타워/잠실)",
        "lat": 37.5131, "lon": 127.1025,
        "desc": "초고층 전망대, 쇼핑몰, 실내 테마파크(롯데월드).",
        "link": "https://english.visitkorea.or.kr"
    },
]

# Folium 지도 생성
m = folium.Map(location=seoul_center, zoom_start=12, tiles="OpenStreetMap")

# 마커 추가
for p in places:
    name = p["name"]
    lat = p["lat"]
    lon = p["lon"]
    desc = p["desc"]
    link = p["link"]

    # 팝업 HTML (작게)
    html = f"""
    <h4>{name}</h4>
    <p>{desc}</p>
    <p><a href="{link}" target="_blank">자세히 보기</a></p>
    """
    iframe = IFrame(html=html, width=260, height=140)
    popup = Popup(iframe, max_width=300)
    folium.Marker(
        location=[lat, lon],
        popup=popup,
        tooltip=name,
    ).add_to(m)

# 지도 렌더링 (streamlit_folium)
st.subheader("📍 Seoul Map (click markers)")
map_data = st_folium(m, width=1100, height=700)

st.markdown("---")
st.info("참고: 위치 좌표는 일반적으로 알려진 중심 좌표를 사용했습니다. 더 정확한 장소 검색/이미지 포함을 원하면 알려줘요! 😊")

st.markdown("**출처(인기 장소 선정 근거)**: TripAdvisor, KoreaToDo, VisitSeoul 등. :contentReference[oaicite:2]{index=2}")
