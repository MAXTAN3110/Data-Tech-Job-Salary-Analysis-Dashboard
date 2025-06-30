from dash import dcc
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
    colors_order = [5, 2, 1, 0, 4, 3]
    colors = [CUSTOM_COLORS[i] for i in colors_order]

    fig = px.treemap(
        salary_median_df,
        path=[px.Constant("World"), "company_location_continent", "company_location"],
        values="salary",
        color="company_location_continent",
        color_discrete_sequence=["rgba(240, 240, 240, 0.8)"] + colors,
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

    new_colors = []
    new_colors.append(fig.data[0]["marker"]["colors"][0])
    count = 0
    for i, customdata in enumerate(fig.data[0].customdata[1:]):
        if customdata[0] == "(?)":
            fig.data[0].customdata[i + 1] = continent_hovercustomdata[count]
            count += 1
            new_colors.append(fig.data[0]["marker"]["colors"][i + 1])
        else:
            new_color = adjusted_rgba(fig.data[0]["marker"]["colors"][i + 1])
            new_colors.append(new_color)

    fig.data[0]["marker"]["colors"] = new_colors
    fig.update_layout(title_x=0.5, title_font_size=18, margin=dict(t=50, b=10))

    # Return the figure
    return dcc.Graph(id="treemap", figure=fig, style={"height": "70vh"})
