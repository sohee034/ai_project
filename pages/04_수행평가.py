# pages/01_company_fat.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FastFood - Most Fatty Items", layout="wide")

st.title("패스트푸드 회사별 '가장 지방(Fat)'한 메뉴 보기")
st.markdown("CSV 파일은 앱 루트에 `FastFoodNutritionMenuV2.csv`로 위치해야 합니다.")

@st.cache_data
def load_data(path: str = "../data/FastFoodNutritionMenuV2.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # 컬럼명 정리: 공백/줄바꿈 제거
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]

    # 영양 컬럼 숫자형으로 변환 (변환 불가 시 NaN)
    num_cols = [
        'Calories', 'Calories from Fat', 'Total Fat (g)', 'Saturated Fat (g)',
        'Trans Fat (g)', 'Cholesterol (mg)', 'Sodium (mg)', 'Carbs (g)',
        'Fiber (g)', 'Sugars (g)', 'Protein (g)'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 총지방 컬럼 이름 추정: 가능한 컬럼명 매핑
    fat_col_candidates = [c for c in df.columns if 'fat' in c.lower() and 'total' in c.lower()]
    if fat_col_candidates:
        fat_col = fat_col_candidates[0]
    else:
        # fallback: 'Total Fat (g)' 존재하지 않으면 첫번째 'Fat' 포함 컬럼 사용
        fat_col = next((c for c in df.columns if 'fat' in c.lower()), None)

    df['fat_col'] = df[fat_col] if fat_col is not None else pd.NA

    # 메뉴별 유니크 처리 (회사, 메뉴명, 지방량)
    if 'Company' in df.columns and 'Item' in df.columns:
        df = df[['Company', 'Item'] + [c for c in df.columns if c not in ['Company','Item']]]

    return df

# 데이터 로드
# 상위 폴더에 CSV 파일이 있을 경우
DATA_PATH = "../FastFoodNutritionMenuV2.csv"  # 루트 폴더 기준  # 앱 루트에 위치
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"CSV 파일을 찾을 수 없습니다: {DATA_PATH}  \n상위 폴더(../)에 위치한지 확인하세요.: {DATA_PATH}  
루트 폴더에 위치한지 확인하세요.")(f"CSV 파일을 찾을 수 없습니다: {DATA_PATH}\n앱 루트에 'FastFoodNutritionMenuV2.csv' 파일을 올려주세요.")
    st.stop()

# 사이드바: 회사 선택
companies = sorted(df['Company'].dropna().unique())
selected_company = st.sidebar.selectbox("Company 선택", companies)

# 사이드바: 몇 개 항목 보기
top_n = st.sidebar.slider("상위 N개 항목 보기 (Total Fat 기준)", min_value=1, max_value=50, value=10)

# 필터링
filtered = df[df['Company'] == selected_company].copy()
filtered = filtered.sort_values('fat_col', ascending=False)

if filtered.empty:
    st.warning("선택한 회사에 대한 데이터가 없습니다.")
    st.stop()

top_items = filtered.head(top_n).copy()

# 색상 설정: 1등 빨간색, 나머지는 파란색에서 투명하게
colors = []
for i in range(len(top_items)):
    if i == 0:
        colors.append('red')
    else:
        # alpha 감소로 그라데이션 효과
        alpha = max(0.15, 1 - (i * (0.8 / max(1, len(top_items)-1))))
        colors.append(f'rgba(0,0,255,{alpha})')

# Plotly 차트
fig = px.bar(
    top_items,
    x='Item',
    y='fat_col',
    hover_data=[col for col in ['Calories','Saturated Fat (g)','Trans Fat (g)','Protein (g)','Sodium (mg)'] if col in top_items.columns],
    labels={'fat_col': 'Total Fat (g)', 'Item': '메뉴'},
    title=f"{selected_company} - 총 지방 기준 상위 {top_n}개 메뉴"
)
fig.update_traces(marker_color=colors, marker_line_width=0.5)
fig.update_layout(title_x=0.5, xaxis_tickangle=-45, yaxis=dict(title='Total Fat (g)'))

st.plotly_chart(fig, use_container_width=True)

# 상세 테이블
st.subheader("상세 정보")
st.dataframe(top_items.reset_index(drop=True))

st.markdown("---")
st.write("CSV 경로:", DATA_PATH)

# 하단: 간단한 설명
st.caption("참고: 데이터의 컬럼명이 dataset 파일에 따라 다를 수 있습니다. 'Total Fat' 관련 컬럼이 자동 매핑되며, 숫자 변환 실패 항목은 NaN으로 처리됩니다.")


