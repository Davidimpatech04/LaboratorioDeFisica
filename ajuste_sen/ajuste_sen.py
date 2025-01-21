import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import altair as alt


def func(list_freq):
    data = pd.DataFrame()
    data["freq"] = list_freq
    lista_bode = []
    for freq in list_freq:
        lista_bode.append(20 * np.log10(2 * np.pi * freq))
    data["bode"] = lista_bode
    return data


def graph(data: pd.DataFrame) -> alt.Chart:
    return (
        alt.Chart(data)
        .mark_point(color="blueviolet")
        .encode(alt.X("Time(s)", title="Time (s)"), y="CH2V")
    )


def f_Sen(x, a, b, c, d):
    return a * np.sin(b * x + c) + d


def regres(data, func=f_Sen, arg=[1.5, 3.14, 0, 2], channel_y="CH2V"):
    x_data = data["Time(s)"]
    y_data = data[channel_y]
    params, cov = curve_fit(f_Sen, x_data, y_data, p0=arg)

    x_regress = np.linspace(x_data.iloc[0], x_data.iloc[-1], 1000)
    y_regress = func(x_regress, *params)

    regres_data = pd.DataFrame()
    regres_data["Time(s)"] = x_regress
    regres_data[channel_y] = y_regress

    return regres_data, params, cov


def data_x_regression(
    data: pd.DataFrame,
    data_regress: pd.DataFrame,
    color_regress="aqua",
    color_p="blueviolet",
    channel_y="CH2V",
) -> alt.Chart:
    ini = data.iloc[0]["Time(s)"]
    final = data.iloc[-1]["Time(s)"]
    graph_data = (
        alt.Chart(data)
        .mark_circle(color=color_p, size=1.5)
        .encode(
            alt.X(
                "Time(s):Q", scale=alt.Scale(domain=[ini, final]), title="Tempo (ms)"
            ),
            alt.Y(channel_y, title="Tensão (V)"),
        )
        .properties(title="Gráfico de Tensão vs Tempo", width=1000, height=200)
    )
    graph_data_regress = (
        alt.Chart(data_regress)
        .mark_line(color=color_regress)
        .encode(
            alt.X(
                "Time(s):Q", scale=alt.Scale(domain=[ini, final]), title="Tempo (ms)"
            ),
            alt.Y(channel_y, title="Tensão (V)"),
        )
        .properties(title="Gráfico de Tensão vs Tempo", width=1000, height=200)
    )

    return graph_data, graph_data_regress
