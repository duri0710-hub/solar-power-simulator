import streamlit as st

st.set_page_config(
    page_title="태양전지 발전량 시뮬레이터",
    page_icon="☀️",
    layout="centered"
)

# 소재별 기준 발전 효율
materials = {
    "단결정 실리콘": 22.0,
    "다결정 실리콘": 18.0,
    "비정질 실리콘": 10.0,
    "페로브스카이트": 25.0,
    "CdTe (카드뮴 텔루라이드)": 19.0,
    "CIGS": 18.0
}

# 제목
st.title("☀️ 태양전지 발전량 시뮬레이터")
st.write("소재에 따른 태양전지의 전기 생산량을 확인해 보세요.")

st.divider()

# 1. 소재 선택
st.subheader("① 소재 선택")

options = list(materials.keys()) + ["나만의 소재 만들기"]

selected = st.selectbox(
    "태양전지 소재를 선택하세요.",
    options
)

if selected == "나만의 소재 만들기":

    material_name = st.text_input(
        "새로운 소재 이름",
        "나만의 태양전지"
    )

    efficiency = st.slider(
        "발전 효율 (%)",
        0.1, 40.0, 20.0, 0.1
    )

    description = st.text_input(
        "소재 특징",
        "직접 설계한 가상의 태양전지 소재"
    )

else:
    material_name = selected
    efficiency = materials[selected]

st.divider()

# 2. 태양전지 면적
st.subheader("② 태양전지 면적 선택")

area = st.slider(
    "태양전지 면적 (㎡)",
    0.1, 10.0, 1.0, 0.1
)

st.divider()

# 3. 일사량
st.subheader("③ 일사량 선택")

irradiance = st.slider(
    "태양광 일사량 (W/㎡)",
    100, 1200, 800, 50
)

sun_hours = 5

st.info("하루 유효 발전 시간은 5시간으로 설정했습니다.")

st.divider()

# 4. 결과 확인
if st.button("📊 결과 확인하기", use_container_width=True):

    energy = (
        area * irradiance * sun_hours * efficiency / 100 / 1000
    )

    st.session_state.result = {
        "name": material_name,
        "efficiency": efficiency,
        "energy": energy,
        "area": area,
        "irradiance": irradiance
    }

# 5. 결과 출력
if "result" in st.session_state:

    r = st.session_state.result

    st.divider()
    st.header("📊 분석 결과")

    st.write(f"**선택한 소재: {r['name']}**")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "하루 에너지 생산량",
            f"{r['energy']:.3f} kWh"
        )

    with col2:
        st.metric(
            "태양광-전기 변환 효율",
            f"{r['efficiency']:.1f}%"
        )

    # 효율별 색상
    if r["efficiency"] < 10:
        color = "#ff4b4b"
        grade = "낮음"

    elif r["efficiency"] < 15:
        color = "#ff914d"
        grade = "보통"

    elif r["efficiency"] < 20:
        color = "#e6c229"
        grade = "양호"

    elif r["efficiency"] < 25:
        color = "#21a366"
        grade = "높음"

    else:
        color = "#3186e8"
        grade = "매우 높음"

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:25px;
            border-radius:15px;
            text-align:center;
            color:white;
        ">
            <h1 style="color:white;">
                {r['efficiency']:.1f}%
            </h1>
            <h3 style="color:white;">
                {grade}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔎 계산 조건")

    st.write(f"- 소재: {r['name']}")
    st.write(f"- 면적: {r['area']}㎡")
    st.write(f"- 일사량: {r['irradiance']}W/㎡")
    st.write(f"- 하루 유효 발전 시간: {sun_hours}시간")

    st.subheader("🧮 계산 공식")

    st.latex(
        r"E = \frac{A \times I \times T \times \eta}{1000}"
    )

    st.caption(
        "※ 소재별 발전 효율은 비교를 위한 예시값입니다. "
        "실제 발전량은 날씨, 온도, 설치 방향 및 발전 손실에 따라 달라집니다."
    )
