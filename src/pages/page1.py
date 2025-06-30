import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.nav_button import create_nav_buttons

dash.register_page(__name__, path="/job-title", name="Job Title")

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1(
                                "What Are the Salary Differences Across Job Titles?",
                                className="font-roboto",
                                style={"fontSize": "2rem"},
                            ),
                            html.H4(
                                "Visualizing Job Title Prevalence",
                                className="font-roboto",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Spinner(
                                                html.Div(
                                                    id="wordcloud_div",
                                                ),
                                                color="primary",
                                            ),
                                        ],
                                    ),
                                ],
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            html.Div(
                                html.H4(
                                    "Unveiling Salary Distributions by Job Category",
                                    className="font-roboto",
                                )
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(
                                            html.Div(id="pie_violin_div"),
                                            color="primary",
                                        ),
                                    ]
                                ),
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            html.Div(
                                html.H4(
                                    "Exploring Salary Trends by Job Category and Experience",
                                    className="font-roboto",
                                )
                            ),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Spinner(
                                            html.Div(id="heatmap_div"), color="primary"
                                        ),
                                    ]
                                ),
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            create_nav_buttons("/", "geo"),
                        ]
                    )
                )
            ],
            fluid=True,
            className="d-flex justify-content-center align-middle",
        )
    ]
)
