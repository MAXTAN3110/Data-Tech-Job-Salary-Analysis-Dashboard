from dash import dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.config import CUSTOM_COLORS
from utils.helper import adjusted_rgba


def create_subplots(df, id):
    counts = df["job_category"].value_counts().sort_values()
    overall_median = df["salary"].median()
    category_median = df.groupby("job_category")["salary"].median()
    category_mean = df.groupby("job_category")["salary"].mean()
    keywords_dict = {
        "Management & Leadership": ["Manager", "Head", "Director"],
        "Machine Learning & AI": ["ML", "AI", "Deep Learning"],
        "Data Engineering & Infrastructure": ["Architect", "Cloud", "ETL"],
        "Business Intelligence": ["BI", "Business", "Finance"],
        "Specialized Roles": ["3D", "Autonomous", "Computer Vision"],
        "Data Science & Analytics": ["Science", "Analyst", "Research"],
    }
    keywords_list = [", ".join(keywords_dict[label]) for label in counts.index]

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "violin"}]],
        horizontal_spacing=0.15,
        column_widths=[0.3, 0.7],
        subplot_titles=[
            "Job Category Breakdown",
            "Salary Distribution Across Job Category",
        ],
    )
    fig.add_trace(
        go.Pie(
            labels=counts.index,
            values=counts.values,
            sort=False,
            direction="clockwise",
            marker=dict(
                colors=CUSTOM_COLORS,
                pattern=dict(shape=["x", "", ".", "-", "/", "\\"]),
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"  # Label (Job Category)
                "Count: %{value}<br>"  # Value (Count)
                "Percentage: %{percent}<br>"  # Percentage
                "Keywords: %{customdata}"  # Add keywords dynamically from customdata
                "<extra></extra>"  # Disable the default extra info in hover box
            ),
            customdata=keywords_list,
            textposition="outside",
            textfont=dict(
                color="black",  # Set the text font color to white
                size=14,  # Optionally, adjust font size
            ),
            legendgroup="group1",
        ),
        row=1,
        col=1,
    )

    for i, label in enumerate(counts.index):
        color = CUSTOM_COLORS[i]
        adjusted_color = adjusted_rgba(color)
        dff = df[df["job_category"] == label]

        fig.add_trace(
            go.Violin(
                y=dff["salary"],
                box_visible=True,
                fillcolor=adjusted_color,
                line_color=color,
                legendgroup="group1",
                name=label,
                showlegend=False,
                hoverinfo="none",
                customdata=[0],
            ),
            row=1,
            col=2,
        )
    fig.update_annotations(yshift=45)

    fig.add_shape(
        type="line",
        x0=-0.5,
        x1=5.5,
        y0=overall_median,
        y1=overall_median,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        ),
        row=1,
        col=2,
    )

    fig.add_annotation(
        x=0.5,  # x position of the arrow's tip
        y=overall_median + 17500,  # y position of the arrow's tip
        text="Overall Median",
        showarrow=True,
        arrowhead=2,  # Arrowhead style
        ax=0,  # x position of the arrow's base
        ay=-50,  # y position of the arrow's base (negative value to move it up)
        font=dict(size=11, color="black"),
        bgcolor="white",  # Background color of the annotation
        bordercolor="black",  # Border color of the annotation
        borderwidth=1,  # Border width of the annotation
        borderpad=4,  # Padding of the border
        opacity=0.8,  # Opacity of the annotation
    )
    fig.update_xaxes(title_text="Job Category", showticklabels=False, row=1, col=2)
    fig.update_yaxes(title_text="Salary (USD)", row=1, col=2)
    fig.update_yaxes(gridcolor="lightgray", zerolinecolor="lightgray", row=1, col=2)

    fig.update_layout(
        margin=dict(b=100),
        legend=dict(
            font=dict(size=18, family="Roboto"),
            entrywidth=0.28,
            entrywidthmode="fraction",
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            bgcolor="#E5ECF6",
        ),
        plot_bgcolor="#F9F9FA",
    )

    return dcc.Graph(
        id=f"pie_violin_plot_{id}",
        figure=fig,
        config={
            "displayModeBar": True,
            "autosizable": True,
            "responsive": True,
            "scrollZoom": True,
        },
        style={"height": "70vh"},
    )
