import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.nav_button import create_nav_buttons

dash.register_page(__name__, path="/company-size", name="Company Size")

layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(
                        [
                            html.H1(
                                "How Company Size Affects Salary Growth Over the Years?",
                                className="font-roboto",
                                style={"fontSize": "2rem"},
                            ),
                            html.H4(
                                "Tracking Salary Growth Trends Relative to Company Size",
                                className="font-roboto",
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Spinner(
                                                html.Div(id="line_bar_div"),
                                                color="primary",
                                            )
                                        ]
                                    ),
                                ],
                                className="card-shadow mb-4",
                                style={"width": "90vw"},
                            ),
                            create_nav_buttons("geo", "/"),
                        ]
                    )
                )
            ],
            fluid=True,
            className="d-flex justify-content-center align-middle",
        )
    ]
)
