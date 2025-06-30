from dash import dcc
import plotly.graph_objects as go
from utils.config import CUSTOM_COLORS


def create_scattergeo(df):
    job_count_df = (
        df.groupby(["company_location_name", "company_location_continent"])
        .agg({"salary": ["median", "count"]})
        .reset_index()
    )
    job_count_df.columns = [
        "company_location_name",
        "company_location_continent",
        "median_salary",
        "job_count",
    ]

    # Create traces for each continent
    continents = df["company_location_continent"].value_counts().index
    colors = {continents[i]: CUSTOM_COLORS[i] for i in range(6)}

    # Create base figure with all traces
    fig = go.Figure()

    # Create a frame for each year
    max_bubble_size = 100

    # Add traces for initial view
    for continent in continents:
        continent_df = job_count_df[
            job_count_df["company_location_continent"] == continent
        ]

        fig.add_trace(
            go.Scattergeo(
                locations=continent_df["company_location_name"],
                locationmode="country names",
                name=continent,
                marker=dict(
                    size=continent_df["job_count"],
                    sizeref=2.0 * max(job_count_df["job_count"]) / (max_bubble_size**2),
                    sizemin=5,
                    sizemode="area",
                    color=colors[continent],
                    line=dict(width=0.5, color="white"),
                ),
                showlegend=True,
                hovertemplate=(
                    "<b>%{location}</b><br>"
                    + "Continent: "
                    + continent
                    + "<br>"
                    + "Median Salary: $%{customdata[0]:,.0f}<br>"
                    + "Total Jobs: %{customdata[1]}<br>"
                    + "<extra></extra>"
                ),
                customdata=continent_df[["median_salary", "job_count"]].values,
            )
        )

    # Update layout
    fig.update_layout(
        title=dict(text="Geographical Distribution of Job Counts Worldwide", x=0.5),
        title_font_size=18,
        margin=dict(t=40, b=0, r=0, l=0),
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="right",
            x=1,
            itemsizing="constant",
            bgcolor="rgb(243, 243, 243)",
        ),
        geo=dict(
            showcoastlines=True,
            projection_type="equirectangular",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
            showocean=True,
            oceancolor="rgb(230, 230, 250)",
        ),
    )

    return dcc.Graph(
        id="scattergeo",
        figure=fig,
        config={
            "displayModeBar": True,
            "autosizable": True,
            "responsive": True,
            "scrollZoom": True,
        },
        style={"height": "70vh"},
    )
