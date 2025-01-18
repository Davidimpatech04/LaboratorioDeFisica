import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import altair as alt
from altair_saver import save


def _f_regres_exp(x, a, b, c):
    return a * np.exp(-b * x) + c


def slicing_data(path, interval, ascending=False) -> pd.DataFrame:
    data = pd.read_csv(path)

    data["Time"] += 0.0025  # Mudando o referencial "0" do tempo
    data["Time"] *= 1000  # segundos -> milissegundos

    ini = interval[0]
    fin = interval[1]

    q = data["Time"].sub(ini).abs().idxmin()
    p = data["Time"].sub(fin).abs().idxmin()

    semi_data = data[q:p]

    idx_min = semi_data["U_b"].idxmin()
    idx_max = semi_data["U_b"].idxmax()
    if ascending:
        filt_data = semi_data.loc[idx_min:idx_max]
    else:
        filt_data = semi_data.loc[idx_max:idx_min]

    return filt_data


def regres_exp(data: pd.DataFrame, func=_f_regres_exp) -> pd.DataFrame:

    x_data = data["Time"]
    y_data = data["U_b"]

    par_optimize, _ = curve_fit(func, x_data, y_data, p0=[1, 1, 1], maxfev=10000)

    _, b, _ = par_optimize

    dado_opt = pd.DataFrame()
    dado_opt["Time"] = x_data
    dado_opt["U_b"] = func(x_data, *par_optimize)

    return dado_opt, b


def data_x_regression(
    data: pd.DataFrame,
    data_regress: pd.DataFrame,
    color_regress="red",
    color_point="blueviolet",
) -> alt.Chart:
    ini = data.iloc[0]["Time"]
    final = data.iloc[-1]["Time"]
    graph_data = (
        alt.Chart(data)
        .mark_circle(color=color_point)
        .encode(
            alt.X("Time:Q", scale=alt.Scale(domain=[ini, final]), title="Tempo (ms)"),
            alt.Y("U_b:Q", title="Tensão (V)"),
        )
        .properties(title="Gráfico de Tensão vs Tempo", width=600, height=400)
    )
    graph_data_regress = (
        alt.Chart(data_regress)
        .mark_line(color=color_regress)
        .encode(
            alt.X("Time:Q", scale=alt.Scale(domain=[ini, final]), title="Tempo (ms)"),
            alt.Y("U_b:Q", title="Tensão (V)"),
        )
        .properties(title="Gráfico de Tensão vs Tempo", width=600, height=400)
    )

    return graph_data + graph_data_regress
