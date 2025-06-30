from plotly.subplots import make_subplots
from dash import dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.helper import adjusted_rgba


def create_linebarplot(df):
    median_salary_df = df.groupby(["work_year", "company_size"], as_index=False)[
        "salary"
    ].median()
    median_salary_df["salary_change_rate"] = (
        median_salary_df.sort_values("work_year")
        .groupby("company_size")["salary"]
        .pct_change()
    )
    median_salary_df["salary_change_rate"] = (
        median_salary_df["salary_change_rate"] * 100
    )

    median_salary_df["mid_work_year"] = median_salary_df["work_year"] - 0.5
    df_clean = median_salary_df.dropna(subset=["salary_change_rate"])
    df_clean["company_size"] = pd.Categorical(
        df_clean["company_size"], categories=["Small", "Medium", "Large"], ordered=True
    )

    company_size_dict = {"Large": "L", "Medium": "M", "Small": "S"}
    legend_label = {
        "Large": "Large (≥250)",
        "Medium": "Medium (51-250)",
        "Small": "Small (<50)",
    }
    cmap = {
        "++": "rgba(16, 140, 20, 1)",
        "+": "rgba(6, 212, 13, 1)",
        "-": "rgba(206, 22, 22, 1)",
    }
    rgba_colors = [
        [cmap[x] for x in ["++", "-", "+"]],
        [cmap[x] for x in ["-", "++", "+"]],
        [cmap[x] for x in ["+", "+", "+"]],
    ]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for i, (label, sub_df) in enumerate(
        df_clean.groupby("company_size", observed=False)
    ):
        fillcolor = [adjusted_rgba(c, 0.6) for c in rgba_colors[i]]
        fig.add_trace(
            go.Bar(
                x=sub_df["mid_work_year"],
                y=sub_df["salary_change_rate"],
                name=label,
                text=company_size_dict[label],
                textposition="auto",
                textangle=0,
                marker_color=fillcolor,
                marker_line_color=rgba_colors[i],
                marker_line_width=1.5,
                showlegend=False,
            ),
            secondary_y=True,
        )

    marker_size_dict = {"Small": 6, "Medium": 15, "Large": 24}
    for label in median_salary_df["company_size"].unique():
        dff = median_salary_df[median_salary_df["company_size"] == label]
        fig.add_trace(
            go.Scatter(
                x=dff["work_year"],
                y=dff["salary"],
                mode="lines+markers",
                name=legend_label[label],
                line=dict(color="rgba(99, 110, 250, 0.5)"),
                marker=dict(size=marker_size_dict[label]),
            )
        )

    fig.update_xaxes(
        title_text="Work Year",
        tickvals=median_salary_df["work_year"].unique(),
        ticktext=[str(year) for year in median_salary_df["work_year"].unique()],
    )
    fig.update_yaxes(
        # title_text="Median Salary (USD)",
        tickvals=np.arange(-100000, 160001, 20000),
        ticktext=[""] * 5 + [f"{i}k" if i != 0 else "0" for i in range(0, 161, 20)],
        range=[-100000, 160000],
        secondary_y=False,
    )
    fig.update_yaxes(
        # title_text="Salary Change Rate (%)",
        tickvals=np.arange(-40, 221, 20),
        ticktext=[str(i) for i in range(-40, 121, 20)] + [""] * 5,
        range=[-40, 220],
        secondary_y=True,
    )
    fig.update_yaxes(gridcolor="lightgray", zerolinecolor="lightgray")

    fig.add_annotation(
        x=-0.045,  # Position to the left of the plot
        y=0.9,  # Centered vertically
        text="Median Salary (USD)",
        textangle=-90,
        showarrow=False,
        xref="paper",
        yref="paper",  # Use normalized coordinates
        xanchor="right",  # Align the text to the right
        yanchor="top",
        font=dict(size=14),
    )

    fig.add_annotation(
        x=0.975,  # Position to the right of the plot
        y=0.1,  # Centered vertically
        text="Salary Change Rate (%)",
        textangle=-90,
        showarrow=False,
        xref="paper",
        yref="paper",
        xanchor="left",  # Align the text to the left
        yanchor="bottom",
        font=dict(size=14),
    )

    fig.update_layout(
        title=dict(
            text="Salary Trends and Yearly Change Rates Across Company Sizes",
            y=0.97,  # Slightly above the top of the plot area
            yanchor="bottom",  # Anchors the title at the bottom to create padding
        ),
        legend_title_text="Company Size",
        legend=dict(yanchor="top", y=1, xanchor="right", x=1.1),
        margin=dict(t=40, b=10, l=75),
        yaxis=dict(showgrid=True, zeroline=False),
        bargap=0.3,
        plot_bgcolor="#F9F9FA",
    )

    # Show the plot
    return dcc.Graph(
        id="line_bar_plot",
        figure=fig,
        config={
            "displayModeBar": True,
            "autosizable": True,
            "responsive": True,
            "scrollZoom": True,
        },
        style={"height": "70vh"},
    )
