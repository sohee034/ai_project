import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 시각화", page_icon="🌍", layout="wide")

# 제목
st.title("🌈 국가별 MBTI 비율 시각화 대시보드")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 선택
countries = sorted(df["Country"].unique())
selected_country = st.selectbox("🌍 국가를 선택하세요:", countries, index=0)

# 선택된 국가 데이터
country_data = df[df["Country"] == selected_country].melt(
    id_vars="Country", var_name="MBTI", value_name="Percentage"
)

# MBTI 비율 순서 정렬
country_data = country_data.sort_values(by="Percentage", ascending=False).reset_index(drop=True)

# 1등 색상 지정: 노란색, 나머지는 파란색 그라데이션
colors = ["#FFD700"] + px.colors.sequential.Blues_r[1:len(country_data)]

# Plotly 그래프
fig = px.bar(
    country_data,
    x="MBTI",
    y="Percentage",
    text="Percentage",
    color="MBTI",
    color_discrete_sequence=colors,
    title=f"🇨🇭 {selected_country}의 MBTI 비율",
)

# 그래프 디자인
fig.update_traces(
    texttemplate="%{text:.2%}",
    textposition="outside",
    hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}",
)
fig.update_layout(
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(tickformat=".0%"),
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 데이터 미리보기
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df)
