from dash import dcc
import plotly.graph_objects as go
from utils.config import CUSTOM_COLORS


def create_scattergeo(df):
    job_count_df = (
        df.groupby(["company_location_name", "company_location_continent", "work_year"])
        .agg({"salary": ["median", "count"]})
        .reset_index()
    )
    job_count_df.columns = [
        "company_location_name",
        "company_location_continent",
        "work_year",
        "median_salary",
        "job_count",
    ]
    job_count_df["cumulative_count"] = job_count_df.groupby(["company_location_name"])[
        "job_count"
    ].cumsum()
    job_count_df = job_count_df.sort_values(by="work_year")

    # Create a list to store frames for animation
    frames = []

    years = sorted(job_count_df["work_year"].unique())

    # Create traces for each continent
    continents = df["company_location_continent"].value_counts().index
    colors = {continents[i]: CUSTOM_COLORS[i] for i in range(6)}

    # Create base figure with all traces
    fig = go.Figure()

    # Create a frame for each year
    max_bubble_size = 15
    for year in years:
        frame_data = []
        for continent in continents:
            year_continent_data = job_count_df[
                (job_count_df["work_year"] == year)
                & (job_count_df["company_location_continent"] == continent)
            ]
            frame_fig = go.Scattergeo(
                locations=year_continent_data["company_location_name"],
                locationmode="country names",
                name=continent,
                marker=dict(
                    size=year_continent_data["cumulative_count"],
                    sizeref=2.0
                    * max(job_count_df["cumulative_count"])
                    / (max_bubble_size**2),  # normalize bubble size
                    sizemin=3,
                    color=colors[continent],
                    line=dict(width=0.5, color="white"),
                ),
                showlegend=False,
                hovertemplate=(
                    "<b>%{location}</b><br>"
                    + "Continent: "
                    + continent
                    + "<br>"
                    + "Median Salary: $%{customdata[0]:,.0f}<br>"
                    + "Jobs This Year: %{customdata[1]}<br>"
                    + "Total Jobs: %{customdata[2]}<br>"
                    + "<extra></extra>"
                ),
                customdata=year_continent_data[
                    ["median_salary", "job_count", "cumulative_count"]
                ].values,
            )

            frame_data.append(frame_fig)

        frames.append(go.Frame(data=frame_data, name=str(year)))

    # Add traces for initial view
    for continent in continents:
        initial_data = job_count_df[
            (job_count_df["work_year"] == years[0])
            & (job_count_df["company_location_continent"] == continent)
        ]

        fig.add_trace(
            go.Scattergeo(
                locations=initial_data["company_location_name"],
                locationmode="country names",
                name=continent,
                marker=dict(
                    size=initial_data["cumulative_count"],
                    sizeref=2.0
                    * max(job_count_df["cumulative_count"])
                    / (max_bubble_size**2),
                    sizemin=3,
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
                    + "Jobs This Year: %{customdata[1]}<br>"
                    + "Total Jobs: %{customdata[2]}<br>"
                    + "<extra></extra>"
                ),
                customdata=initial_data[
                    ["median_salary", "job_count", "cumulative_count"]
                ].values,
            )
        )

    # Update layout
    fig.update_layout(
        title=dict(text="Global Salary Distribution Over Time", x=0.5),
        title_font_size=18,
        showlegend=True,
        margin=dict(t=40, b=0, r=0, l=0),
        legend=dict(yanchor="top", y=1, xanchor="right", x=0.975, bgcolor="#E5ECF6"),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
            showocean=True,
            oceancolor="rgb(230, 230, 250)",
            scope="world",
            lataxis_range=[-90, 90],
            lonaxis_range=[-180, 180],
        ),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 500},
                            },
                        ],
                        "label": "▶",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "▐▐",
                        "method": "animate",
                    },
                ],
                "direction": "left",
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "left",
                "y": -0.13,
                "yanchor": "bottom",
            }
        ],
        sliders=[
            {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Year: ",
                    "visible": False,
                    "xanchor": "right",
                },
                "transition": {"duration": 300, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 30},
                "len": 0.6,
                "x": 0.2,
                # "y": 0,
                "steps": [
                    {
                        "args": [
                            [str(year)],
                            {
                                "frame": {"duration": 1000, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 500},
                            },
                        ],
                        "label": str(year),
                        "method": "animate",
                    }
                    for year in years
                ],
            }
        ],
    )

    # Add frames to the figure
    fig.frames = frames

    return dcc.Graph(
        id="geoscatter",
        figure=fig,
        config={
            "displayModeBar": True,
            "autosizable": True,
            "responsive": True,
            "scrollZoom": True,
        },
        style={"height": "80vh"},
    )
