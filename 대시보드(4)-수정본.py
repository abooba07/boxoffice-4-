import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="역대 박스오피스 대시보드", page_icon="🎬", layout="wide")
st.title("🎬 역대 흥행 영화 데이터 분석")
st.caption("출처: 영화진흥위원회 통합전산망 · 조회일: 2026-06-02")
st.markdown("---")

@st.cache_data
def load_data():
    movie = pd.read_csv("역대박스오피스.csv", skiprows=4, encoding="utf-8")
    cols = ["매출액", "관객수", "스크린수", "상영횟수"]
    for c in cols:
        movie[c] = pd.to_numeric(movie[c].astype(str).str.replace(",", ""), errors="coerce")
    movie = movie.dropna(subset=cols + ["영화명", "대표국적"])
    movie["매출액_억"] = movie["매출액"] / 1e8
    movie["관객수_백만"] = movie["관객수"] / 1e6
    return movie

try:
    movie = load_data()
except Exception as e:
    st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 색상 규칙: 한국=주황, 나머지=회색
color_map = {"한국": "#E67E22", "미국": "#6C7A89", "일본": "#27AE60"}

# 기본 통계
st.subheader("📊 기본 통계")
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 영화 수", f"{len(movie)}편")
col2.metric("평균 관객수", f"{movie['관객수'].mean():,.0f}명", f"최대 {movie['관객수'].max():,.0f}명")
col3.metric("평균 스크린수", f"{movie['스크린수'].mean():.1f}개", f"최대 {movie['스크린수'].max():.0f}개")
col4.metric("평균 상영횟수", f"{movie['상영횟수'].mean():,.0f}회", f"최대 {movie['상영횟수'].max():.0f}회")
st.markdown("---")

# TOP 10 (매출 기준)
top10 = movie.sort_values(by="매출액", ascending=False).head(10)

st.subheader("💰 TOP 10 - 매출액 (억 원)")
fig1 = px.bar(
    top10.sort_values("매출액_억", ascending=False),
    x="영화명", y="매출액_억", color="대표국적",
    color_discrete_map=color_map,
    labels={"매출액_억": "억 원", "영화명": ""}
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("👥 TOP 10 - 관객수 (백만 명)")
fig2 = px.bar(
    top10.sort_values("관객수_백만", ascending=False),
    x="영화명", y="관객수_백만", color="대표국적",
    color_discrete_map=color_map,
    labels={"관객수_백만": "백만 명", "영화명": ""}
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🎬 TOP 10 - 스크린수 (개)")
fig3 = px.bar(
    top10.sort_values("스크린수", ascending=False),
    x="영화명", y="스크린수", color="대표국적",
    color_discrete_map=color_map,
    labels={"스크린수": "개", "영화명": ""}
)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📅 TOP 10 - 상영횟수 (회)")
fig4 = px.bar(
    top10.sort_values("상영횟수", ascending=False),
    x="영화명", y="상영횟수", color="대표국적",
    color_discrete_map=color_map,
    labels={"상영횟수": "회", "영화명": ""}
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# 대표국적 파이차트 + 관객수 분포
st.subheader("🌏 대표국적 분포  &  관객수 분포")
col_left, col_right = st.columns(2)

with col_left:
    country = movie["대표국적"].value_counts().reset_index()
    country.columns = ["국적", "영화 수"]
    fig5 = px.pie(
        country, names="국적", values="영화 수",
        title="대표국적 분포", hole=0.4,
        color="국적", color_discrete_map=color_map
    )
    st.plotly_chart(fig5, use_container_width=True)

with col_right:
    fig6 = px.histogram(
        movie, x="관객수_백만", nbins=10,
        title="관객수 분포 (백만 명 단위)",
        labels={"관객수_백만": "백만 명", "count": "영화 수"},
        color_discrete_sequence=["#7F8C8D"]
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.caption("프로그램이 정상적으로 종료되었습니다.")
