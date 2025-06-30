import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.nav_button import create_nav_buttons

dash.register_page(__name__, path="/geo", name="Geographical")

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1(
                                "Which Regions Offer the Highest Incomes?",
                                className="font-roboto",
                                style={"fontSize": "2rem"},
                            ),
                            html.H4(
                                "Mapping Salary Variations Across the Globe",
                                className="font-roboto",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Spinner(
                                                html.Div(id="treemap_div"),
                                                color="primary",
                                            )
                                        ]
                                    ),
                                ],
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            html.Div(
                                html.H4(
                                    "Exploring Potential Bias in Regional Data Representation",
                                    className="font-roboto",
                                )
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Spinner(
                                                html.Div(id="scattergeo_div"),
                                                color="primary",
                                            )
                                        ]
                                    ),
                                ],
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            create_nav_buttons("job-title", "company-size"),
                        ]
                    )
                )
            ],
            fluid=True,
            className="d-flex justify-content-center align-middle",
        )
    ]
)
