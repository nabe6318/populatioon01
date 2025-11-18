import math
import pandas as pd
import streamlit as st
import altair as alt

# ---------------------------------------
# 画面設定
# ---------------------------------------
st.set_page_config(page_title="個体群増加モデル（指数増加）雑草学専用", layout="wide")

st.markdown(
    "<h3 style='font-size:22px; color:#333;'>個体群の増加モデル（雑草学・指数増加）</h3>",
    unsafe_allow_html=True
)
st.write("サイドバーの入力欄で N₀（初期個体数）と r（内的増殖率）を直接入力できます。")

st.latex(r"N_t = N_0 e^{rt}")

# ---------------------------------------
# サイドバー（slider → number_input）
# ---------------------------------------
st.sidebar.header("パラメータ設定")

N0 = st.sidebar.number_input(
    "N₀（初期個体数）",
    min_value=0,
    max_value=100000,
    value=100,    # デフォルト
    step=10,
)

r = st.sidebar.number_input(
    "r（内的増殖率）",
    min_value=-5.0,   # 減少モデルも扱えるように負も許可
    max_value=5.0,
    value=0.2,        # デフォルト
    step=0.01,
    format="%.3f"
)

t_max = st.sidebar.number_input(
    "t の最大値（期間）",
    min_value=1,
    max_value=10000,
    value=20,
    step=1,
)

# ---------------------------------------
# 計算
# ---------------------------------------
t_values = list(range(int(t_max) + 1))
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


