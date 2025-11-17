import math
import pandas as pd
import streamlit as st
import altair as alt

# ---------------------------------------
# 画面設定
# ---------------------------------------
st.set_page_config(page_title="個体群増加モデル（指数増加）", layout="wide")

st.markdown(
    "<h3 style='font-size:22px; color:#333;'>個体群の増加モデル（指数増加）</h3>",
    unsafe_allow_html=True
)
st.write("サイドバーのスライダーで N₀（初期個体数）と r（内的増殖率）を調整できます。")

st.latex(r"N_t = N_0 e^{rt}")

# ---------------------------------------
# サイドバー（左）にスライダー配置
# ---------------------------------------
st.sidebar.header("パラメータ設定")

N0 = st.sidebar.slider(
    "N₀（初期個体数）",
    min_value=0,
    max_value=1000,
    value=100,       # デフォルト
    step=10,
)

r = st.sidebar.slider(
    "r（内的増殖率）",
    min_value=0.0,
    max_value=1.0,
    value=0.2,       # デフォルト
    step=0.01,
)

t_max = st.sidebar.slider(
    "t の最大値（期間）",
    min_value=1,
    max_value=100,
    value=20,
    step=1,
)

# ---------------------------------------
# 計算
# ---------------------------------------
t_values = list(range(t_max + 1))
Nt_values = [N0 * math.exp(r * t) for t in t_values]

df = pd.DataFrame({"t": t_values, "N": Nt_values})

# ---------------------------------------
# テーブル表示
# ---------------------------------------
st.subheader("計算結果（テーブル）")
st.dataframe(df.style.format({"N": "{:.3f}"}), use_container_width=True)

# ---------------------------------------
# グラフ（Altair）
# ---------------------------------------
st.subheader("時間とともに変化する個体数 N のグラフ")

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("t:Q", title="t（時間）"),
        y=alt.Y("N:Q", title="N（個体数）"),
    )
    .properties(height=400)
)

st.altair_chart(chart, use_container_width=True)

