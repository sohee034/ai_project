# pages/01_company_fat.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FastFood - Most Fatty Items", layout="wide")

st.title("🍔 패스트푸드 회사별 '가장 지방(Fat)'한 메뉴 보기")
st.markdown("👉 CSV 파일은 앱 루트 폴더에 `FastFoodNutritionMenuV2.csv` 로 위치해야 합니다.")

# --------------------------
# 데이터 로드 함수
# --------------------------
@st.cache_data
def load_data(path: str = "../FastFoodNutritionMenuV2.csv") -> pd.DataFrame:
    df = pd.read_csv(path)

    # 컬럼명 정리: 공백/줄바꿈 제거
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]

    # 숫자형 변환
    num_cols = [
        'Calories', 'Calories from Fat', 'Total Fat (g)', 'Saturated Fat (g)',
        'Trans Fat (g)', 'Cholesterol (mg)', 'Sodium (mg)', 'Carbs (g)',
        'Fiber (g)', 'Sugars (g)', 'Protein (g)'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 총 지방 컬럼 자동 탐색
    fat_col_candidates = [c for c in df.columns if 'fat' in c.lower() and 'total' in c.lower()]
    if fat_col_candidates:
        fat_col = fat_col_candidates[0]
    else:
        fat_col = next((c for c in df.columns if 'fat' in c.lower()), None)

    df['fat_col'] = df[fat_col] if fat_col is not None else pd.NA

    return df

# --------------------------
# CSV 로드
# --------------------------
DATA_PATH = "../FastFoodNutritionMenuV2.csv"

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"❌ CSV 파일을 찾을 수 없습니다: {DATA_PATH}\n"
        f"⚠️ CSV 파일은 반드시 앱 루트 폴더에 'FastFoodNutritionMenuV2.csv' 로 위치해야 합니다.\n"
        f"📁 (pages 폴더의 상위 폴더)"
    )
    st.stop()

# --------------------------
# 사이드바 옵션
# --------------------------
companies = sorted(df['Company'].dropna().unique())
selected_company = st.sidebar.selectbox("🔍 Company 선택", companies)

top_n = st.sidebar.slider(
    "📊 상위 N개 항목 보기 (Total Fat 기준)",
    min_value=1,
    max_value=50,
    value=10
)

# 필터링
filtered = df[df['Company'] == selected_company].sort_values('fat_col', ascending=False)

if filtered.empty:
    st.warning("선택한 회사에 대한 데이터가 없습니다.")
    st.stop()

top_items = filtered.head(top_n)

# --------------------------
# 색상 세팅: 1등=빨강 / 나머지=파란색 투명도 감소
# --------------------------
colors = []
for i in range(len(top_items)):
    if i == 0:
        colors.append("red")
    else:
        alpha = max(0.15, 1 - (i * (0.8 / max(1, len(top_items)-1))))
        colors.append(f"rgba(0,0,255,{alpha})")

# --------------------------
# Plotly 그래프
# --------------------------
fig = px.bar(
    top_items,
    x="Item",
    y="fat_col",
    hover_data=[c for c in ['Calories', 'Saturated Fat (g)', 'Trans Fat (g)', 'Protein (g)', 'Sodium (mg)'] if c in top_items.columns],
    labels={"fat_col": "Total Fat (g)", "Item": "메뉴"},
    title=f"🍟 {selected_company} - 지방(Fat) 함량 상위 {top_n}개 메뉴"
)

fig.update_traces(marker_color=colors, marker_line_width=0.5)
fig.update_layout(
    title_x=0.5,
    xaxis_tickangle=-45,
    yaxis_title="Total Fat (g)"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 상세 테이블
# --------------------------
st.subheader("📄 상세 정보 테이블")
st.dataframe(top_items.reset_index(drop=True))

st.markdown("---")
st.caption(f"📂 CSV 경로 사용됨: {DATA_PATH}")
st.caption("⚠️ 컬럼명은 데이터 파일 구조에 따라 자동 매핑됩니다. Total Fat 관련 컬럼 자동 탐색 기능 포함.")

