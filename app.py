import streamlit as st
import pandas as pd
import plotly.express as px
import io

# -------------------
# 1. 페이지 기본 설정
# -------------------
st.set_page_config(page_title="데이터 시각화 웹앱", page_icon="📊", layout="centered")

st.title("📊 간편한 데이터 시각화 도구")
st.caption("제미나이 데이터 입력부터 엑셀 스타일의 수정, 다양한 그래프 디자인까지 한 번에!")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# -------------------
# 1단계: 데이터 입력
# -------------------
with st.expander("✍️ 1) 입력", expanded=True):
    st.markdown("#### 🤖 제미나이 데이터 자동 입력")
    st.info("제미나이가 생성한 텍스트(표 형태의 데이터, CSV 등)를 통째로 붙여넣으세요.")
    
    raw_text = st.text_area("데이터 입력란", placeholder="[예시]\n연도,서울 아파트 가격\n2020,80000\n2021,95000\n2022,90000\n2023,88000", height=150)
    
    if st.button("🪄 AI 데이터 자동 완성하기 (파싱)", use_container_width=True):
        if raw_text:
            try:
                if '\t' in raw_text:
                    st.session_state.df = pd.read_csv(io.StringIO(raw_text), sep='\t')
                else:
                    st.session_state.df = pd.read_csv(io.StringIO(raw_text), sep=',')
                st.success("데이터가 성공적으로 파싱되었습니다! '2) 데이터수정' 탭을 확인하세요.")
            except Exception as e:
                st.error(f"데이터 파싱 중 오류가 발생했습니다: {e}\n형식을 다시 확인해주세요.")
        else:
            st.warning("데이터를 먼저 입력해주세요.")

# -------------------
# 2단계: 데이터 수정
# -------------------
with st.expander("📊 2) 데이터수정"):
    if not st.session_state.df.empty:
        st.markdown("엑셀처럼 표를 직접 클릭하여 **수정, 행/열 추가 및 삭제**가 가능합니다.")
        st.session_state.df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
    else:
        st.write("아직 입력된 데이터가 없습니다. 1단계에서 데이터를 입력해주세요.")

# -------------------
# 3단계: 디자인
# -------------------
with st.expander("🎨 3) 디자인"):
    if not st.session_state.df.empty:
        df = st.session_state.df
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.selectbox("그래프 종류 선택", ["선 그래프", "막대 그래프", "원 그래프 (파이차트)", "산점도 (Scatter)"])
        
        with col2:
            x_col = st.selectbox("X축 (또는 기준) 데이터", columns, index=0)
            y_col = st.selectbox("Y축 (또는 값) 데이터", columns, index=1 if len(columns)>1 else 0)

        fig = None
        try:
            if chart_type == "선 그래프":
                fig = px.line(df, x=x_col, y=y_col, title=f"{x_col}에 따른 {y_col} (선 그래프)")
            elif chart_type == "막대 그래프":
                fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col}에 따른 {y_col} (막대 그래프)")
            elif chart_type == "원 그래프 (파이차트)":
                fig = px.pie(df, names=x_col, values=y_col, title=f"{x_col} 기준 {y_col} 비율 (원 그래프)")
            elif chart_type == "산점도 (Scatter)":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col}와 {y_col}의 상관관계")
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                st.session_state.fig = fig
        except Exception as e:
            st.error("그래프를 그리는 중 오류가 발생했습니다. 축 데이터를 확인하세요.")
    else:
        st.write("데이터가 없습니다.")

# -------------------
# 4단계: 저장
# -------------------
with st.expander("💾 4) 저장"):
    if 'fig' in st.session_state and st.session_state.fig is not None:
        st.markdown("완성된 데이터와 그래프를 저장할 수 있습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            csv = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 수정된 데이터(CSV) 다운로드",
                data=csv,
                file_name="modified_data.csv",
                mime="text/csv",
            )
        with col2:
            st.info("💡 팁: 그래프 이미지 저장은 그래프 우측 상단 메뉴(카메라 아이콘)를 클릭하세요.")
    else:
        st.write("저장할 그래프가 없습니다. 3단계를 먼저 진행해주세요.")
