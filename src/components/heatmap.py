import pandas as pd
from dash import dcc
import plotly.graph_objects as go


def create_heatmap(df):
    df["experience_level"] = pd.Categorical(
        df["experience_level"],
        categories=["Entry", "Intermediate", "Senior", "Executive"],
        ordered=True,
    )

    index_list = [
        "Data Science & Analytics",
        "Data Engineering & Infrastructure",
        "Machine Learning & AI",
        "Management & Leadership",
        "Business Intelligence",
        "Specialized Roles",
    ]

    pivot_table = df.pivot_table(
        values="salary",
        index="job_category",
        columns="experience_level",
        aggfunc="median",
        observed=False,
    )
    pivot_table = pivot_table.reindex(index_list)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_table.values,  # Salary values for heatmap
            x=pivot_table.columns,  # Experience levels (columns)
            y=pivot_table.index,  # Job categories (rows)
            colorscale="GnBu",  # Color scheme
            zmin=pivot_table.min().min(),  # Minimum salary value
            zmax=pivot_table.max().max(),  # Maximum salary value
            colorbar=dict(title="Median Salary (USD)"),
        )
    )

    # Add annotations for each cell (optional, for displaying values in each cell)
    annotations = []
    for i, row in enumerate(pivot_table.index):
        for j, col in enumerate(pivot_table.columns):
            annotations.append(
                dict(
                    x=col,
                    y=row,
                    text=(
                        str(int(round(pivot_table.loc[row, col])))
                        if not pd.isna(pivot_table.loc[row, col])
                        else ""
                    ),
                    showarrow=False,
                    font=dict(
                        color=(
                            "black"
                            if (pivot_table.loc[row, col] <= 160000)
                            else "white"
                        )
                    ),
                )
            )

    xstart = 0
    xmax = 3
    padding = 0.05
    ypos = -0.15

    annotations.append(
        dict(
            x=xmax,
            y=ypos,
            ax=xstart - padding,
            ay=ypos,
            xref="x",
            axref="x",
            yref="paper",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="#9A9A9A",
        )
    )
    # Add labels for "Low" and "High" on each side of the arrow
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.09,
            y=-0.145,
            text="Low",
            showarrow=False,
            font=dict(size=14),
        )
    )
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.91,
            y=-0.145,
            text="High",
            showarrow=False,
            font=dict(size=14),
        )
    )

    fig.update_xaxes(title_font_size=30)
    fig.update_yaxes(title_font_size=30)
    fig.update_layout(
        title="Median Salary Heatmap by Job Category and Experience",
        margin=dict(t=40, b=80),
        xaxis_title="Experience Level",
        yaxis_title="Job Category",
        annotations=annotations,
        plot_bgcolor="#F9F9FA",
    )

    return dcc.Graph(id="heatmap", figure=fig, style={"height": "70vh"})
