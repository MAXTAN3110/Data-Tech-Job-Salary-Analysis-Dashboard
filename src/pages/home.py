import dash
from dash import html
from components.donut import DonutChart
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/", name="Home")

graph_data = [
    {
        "label": "Geographical Location",
        "value": 33,
        "path": "/geo",
        "icon": "mdi:map-marker-outline",
    },
    {
        "label": "Company Size",
        "value": 33,
        "path": "/company-size",
        "icon": "mdi:office-building-outline",
    },
    {
        "label": "Job Title",
        "value": 33,
        "path": "/job-title",
        "icon": "mdi:briefcase-outline",
    },
]

layout = html.Div(
    id="home-page",
    children=[
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H1(
                                                "Data Tech Job Salary Analysis Dashboard",
                                                className="text-center",
                                                style={"font-family": "Roboto"},
                                            ),
                                            DashIconify(
                                                icon="tabler:device-analytics",
                                                color="#02a4cc",
                                                height=50,
                                                width=60,
                                                inline=True,
                                            ),
                                        ],
                                        className="d-flex justify-content-center align-middle gap-2",
                                    ),
                                    html.H2(
                                        "Extract Field-wise Insights and Trends",
                                        className="text-center",
                                        style={"font-family": "Roboto"},
                                    ),
                                ],
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Div([], style={"height": "5vh"}),
                                            DonutChart(
                                                id="my-donut-graph",
                                                data=graph_data,
                                                centerText="Key Factors of Salary",
                                            ),
                                        ],
                                        style={"height": "100%"},
                                    ),
                                ],
                                className="card-shadow",
                                style={"height": "60vh", "width": "90vw"},
                            ),
                        ]
                    ),
                    justify="center",
                ),
            ],
            fluid=True,
            className="d-flex justify-content-center align-middle",
        ),
    ],
)
