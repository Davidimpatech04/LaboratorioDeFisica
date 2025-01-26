import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import altair as alt


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


def data_vr(path: pd.DataFrame, paramvr) -> pd.DataFrame:
    def func_sen(x, a, b, c, d):
        return a * np.sin(b * x + c) + d

    df = pd.read_csv(path)
    Data_vr = pd.DataFrame()
    df["Time(s)"] *= 1000
    Data_vr["U"] = func_sen(
        df["Time(s)"], paramvr[1], paramvr[3], paramvr[5], paramvr[7]
    ) - func_sen(df["Time(s)"], paramvr[0], paramvr[2], paramvr[4], paramvr[6])
    Data_vr["Time(s)"] = df["Time(s)"]
    Data_vr = Data_vr.dropna()
    return Data_vr


def process(path, argw=[1.5, 3.14, 0, 2], channel_ys="CH2V", cr="red"):
    if channel_ys == "CH1V":
        color_point = "green"
    elif channel_ys == "U":
        color_point = "brown"
    else:
        color_point = "blueviolet"

    if type(path) != pd.DataFrame:
        df = pd.read_csv(path)

        df["Time(s)"] *= 1000

    else:
        df = path

    r_data, param, cov = regres(df, arg=argw, channel_y=channel_ys)

    graph_data, graph_regres = data_x_regression(
        df, r_data, channel_y=channel_ys, color_p=color_point, color_regress=cr
    )

    return graph_data, graph_regres, param, cov


def save_datas(
    path_data,
    path_save,
    pathimg1,
    pathimg2,
    argww=[3, 3.14, -1, 10],
    argwww=[3, 3.14, -100, -10],
    argvr=[3, 3.14, -100, -10],
    RL=False,
    RLC=False,
):

    a1, a2, parametros_Vc, cov_vc = process(path_data, argww, cr="blue")
    avc, bvc, cvc, dvc = parametros_Vc
    if not RL and not RLC:
        legend_a1 = (
            alt.Chart(
                pd.DataFrame(
                    {
                        "Category": ["VC", "Vg", "VR"],
                        "Color": ["blue", "yellow", "green"],
                    }
                )
            )
            .mark_point()
            .encode(
                y=alt.Y("Category", axis=alt.Axis(title="Legend")),
                color=alt.Color("Color:N", scale=None),
            )
        )
    elif RL:
        legend_a1 = (
            alt.Chart(
                pd.DataFrame(
                    {
                        "Category": ["VL", "Vg", "VR"],
                        "Color": ["blue", "yellow", "green"],
                    }
                )
            )
            .mark_point()
            .encode(
                y=alt.Y("Category", axis=alt.Axis(title="Legend")),
                color=alt.Color("Color:N", scale=None),
            )
        )
    else:
        legend_a1 = (
            alt.Chart(
                pd.DataFrame(
                    {
                        "Category": ["VLC", "Vg", "VR"],
                        "Color": ["blue", "yellow", "green"],
                    }
                )
            )
            .mark_circle()
            .encode(
                y=alt.Y("Category", axis=alt.Axis(title="Legend")),
                color=alt.Color("Color:N", scale=None),
            )
        )
    # a1.display()
    # (a1 + a2).display()

    a3, a4, parametros_Vg, cov_vg = process(
        path_data, argwww, channel_ys="CH1V", cr="orange"
    )
    avg, bvg, cvg, dvg = parametros_Vg
    # a3.display()
    # (a3 + a4).display()
    # (a2 + a4).display()

    vr = data_vr(path_data, [avc, avg, bvc, bvg, cvc, cvg, dvc, dvg])

    a5, a6, parametros_vr, cov_vr = process(vr, argvr, channel_ys="U", cr="green")
    avr, bvr, cvr, dvr = parametros_vr

    # a5.display()
    # (a5 + a6).display()

    (a1 + a3 + a5).display()
    ((a1 + a3 + a5) | legend_a1).save(pathimg1)
    ((a2 + a4 + a6) | legend_a1).display()
    ((a2 + a4 + a6) | legend_a1).save(pathimg2)

    with open(path_save, "w") as f:
        f.write(f"Vg:\n")
        f.write(f"funcao Vg = {avg}*sen({bvg}x + {cvg}) + {dvg}\n")
        f.write(f"Matriz de covariancia VG:\n")
        f.write(f"{np.sqrt(np.diag(cov_vg))}\n")
        f.write(f"Vc:\n")
        f.write(f"funcao Vc = {avc}*sen({bvc}x + {cvc}) + {dvc}\n")
        f.write(f"Matriz de covariancia VC:\n")
        f.write(f"{np.sqrt(np.diag(cov_vc))}\n")
        f.write(f"Vr:\n")
        f.write(f"funcao Vr = {avr}*sen({bvr}x + {cvr}) + {dvr}\n")
        f.write(f"Matriz de covariancia VR:\n")
        f.write(f"{np.sqrt(np.diag(cov_vr))}")
