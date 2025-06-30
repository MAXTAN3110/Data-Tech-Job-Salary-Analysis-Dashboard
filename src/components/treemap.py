from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from utils.config import CUSTOM_COLORS
from utils.helper import adjusted_rgba


def create_treemap(df):
    dff = df[df["company_location"] != "IL"]
    # Median for each country
    salary_median_df = (
        dff.groupby(
            ["company_location_continent", "company_location", "company_location_name"]
        )["salary"]
        .median()
        .reset_index()
    )
    # Median for each continent
    continent_medians = (
        dff.groupby("company_location_continent")["salary"].median().to_dict()
    )
    # Median for the whole world
    total_median = dff["salary"].median()
    colors_order = [2, 1, 3, 4, 5, 0]
    colors = [CUSTOM_COLORS[i] for i in colors_order]
    fig = px.treemap(
        salary_median_df,
        path=[px.Constant("World"), "company_location_continent", "company_location"],
        values="salary",
        color="company_location_continent",
        color_discrete_sequence=colors + ["rgba(205, 205, 209, 0.5)"],
        title="Median Salary Treemap by Continents and Countries",
        custom_data=["company_location_name", "salary", "company_location_continent"],
    )

    # Create custom hover template
    hover_template = (
        "<b>Country:</b> %{customdata[0]}<br>"
        + "<b>Median Salary:</b> $%{customdata[1]:,.0f}<br>"
        + "<b>Continent:</b> %{customdata[2]}"
    )

    # Update the traces to show values in currency format
    fig.update_traces(
        texttemplate="%{label}<br>$%{value:,.0f}",
        textposition="middle center",
        hovertemplate=hover_template,
        marker_line_color="grey",
    )
    # Update the hoverinfo for continents and world
    continent_hovercustomdata = [["", v, k] for k, v in continent_medians.items()]
    continent_hovercustomdata.append(["", total_median, ""])
    fig.data[0].customdata[-7:] = continent_hovercustomdata

    # Adjust the color for children node
    orig_colors = fig.data[0]["marker"]["colors"]
    new_colors = []
    for i in range(len(orig_colors) - 7):
        color = orig_colors[i]
        new_colors.append(adjusted_rgba(color, 0.4))
    new_colors.extend(orig_colors[-7:])
    fig.data[0]["marker"]["colors"] = new_colors

    fig.update_layout(title_x=0.5, title_font_size=18, margin=dict(t=50, b=10))

    # Return the figure
    return dcc.Graph(id="treemap", figure=fig, style={"height": "70vh"})
