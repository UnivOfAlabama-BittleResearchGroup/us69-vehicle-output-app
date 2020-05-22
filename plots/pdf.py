import os
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from index import APP_PATH
import numpy as np

data_dir = os.path.join(APP_PATH, 'data', 'sample_analysis')


def plot_pdf(sample_percent1, sample_percent2, plot_var, plot_var2):
    df1 = pd.read_csv(os.path.join(data_dir, sample_percent1, 'data_summary.csv'), header=[0, 1], index_col=0)
    df2 = pd.read_csv(os.path.join(data_dir, sample_percent2, 'data_summary.csv'), header=[0, 1], index_col=0)

    label1 = sample_percent1 + ' Percent'
    label2 = sample_percent2 + ' Percent'

    group_labels = [label1, label2]

    colors = ['slategray', 'magenta']

    x1 = df1[(plot_var, plot_var2)].iloc[2:].replace([np.inf, -np.inf], np.nan)
    x2 = df2[(plot_var, plot_var2)].iloc[2:].replace([np.inf, -np.inf], np.nan)

    x1 = x1.dropna()
    x2 = x2.dropna()

    bin_size = round((max(x1 + x2) - min(x1 + x2)) / 100, 2)
    # try:
    fig = ff.create_distplot([x1, x2], group_labels, bin_size=bin_size,
                                 curve_type='normal',
                                 histnorm='probability density',  # override default 'kde'
                                 colors=colors)
    # except RuntimeError:
    #     print('help')
    #     x = 1

    fig.add_annotation(
        x=df1[(plot_var, plot_var2)].iloc[1],
        y=fig._data[2]['y'].max(),
        text=f"Mean Value of {sample_percent1}% is {round(df1[(plot_var, plot_var2)].iloc[1], 3)}",
        showarrow=True,
        arrowhead=7,
        ax=-40,
        ay=-40,
    )
    fig.add_annotation(
        x=df2[(plot_var, plot_var2)].iloc[1],
        y=fig._data[3]['y'].max(),
        text=f"Mean Value of {sample_percent2}% is {round(df2[(plot_var, plot_var2)].iloc[1], 3)}",
        showarrow=True,
        arrowhead=7,
        ax=40,
        ay=-60
    )

    # fig.update_annotations([dict(
    #     xref="x",
    #     yref="y",
    #     showarrow=True,
    #     arrowhead=7,
    #     ax=-20,
    #     ay=-40
    # ),
    #     dict(
    #         xref="x",
    #         yref="y",
    #         showarrow=True,
    #         arrowhead=7,
    #         ax=20,
    #         ay=-40
    #     )
    # ])

    return fig
