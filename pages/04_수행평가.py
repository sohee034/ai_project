import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Most Fatty Menu by Company", layout="wide")

st.title("🍔 패스트푸드 회사별 가장 지방(Fat)이 높은 메뉴")
st.write("CSV 파일은 반드시 앱 루트에 `fastfood.csv` 로 위치해야 합니다.")

# -----------------------
# 📂 CSV 불러오기
# -----------------------
@st.cache_data
def load_data():
    # CSV 파일명 변경 적용
    df = pd.read_csv("../fastfood.csv")

    # 컬럼명 정리 (줄바꿈 제거)
    df.columns = [c.replace("\n", " ").strip() for c in df.columns]

    # 숫자형 컬럼 변환
    numeric_cols = [
        "Calories", "Calories from Fat", "Total Fat (g)", "Saturated Fat (g)",
        "Trans Fat (g)", "Cholesterol (mg)", "Sodium (mg)", "Carbs (g)",
        "Fiber (g)", "Sugars (g)", "Protein (g)", "Weight Watchers Pnts"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# -----------------------
# 🏢 회사 선택 UI
# -----------------------
companies = sorted(df["Company"].dropna().unique())
company = st.selectbox("회사 선택", companies)

filtered = df[df["Company"] == company].copy()

if filtered.empty:
    st.warning("해당 회사의 데이터가 없습니다.")
    st.stop()

# -----------------------
# 🥇 가장 Fat 높은 메뉴 찾기
# -----------------------
top_item = (
    filtered.sort_values("Total Fat (g)", ascending=False)
            .head(1)
)

st.subheader(f"🏆 **{company}** 의 가장 Fat(지방)이 높은 메뉴")
st.write(top_item[["Item", "Total Fat (g)", "Calories", "Sodium (mg)", "Protein (g)"]])

# -----------------------
# 📊 Plotly 시각화
# -----------------------
st.subheader("📊 회사 내 Top 10 지방 높은 메뉴")

top10 = (
    filtered.sort_values("Total Fat (g)", ascending=False)
            .head(10)
)

fig = px.bar(
    top10,
    x="Item",
    y="Total Fat (g)",
    title=f"{company} 지방(Fat) Top 10 메뉴",
    hover_data=["Calories", "Sodium (mg)", "Protein (g)"],
    template="plotly_white"
)
