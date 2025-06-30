import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def create_nav_buttons(prev_href=None, next_href=None):
    nav_buttons = dbc.Row(
        [
            # Back button
            dbc.Col(
                dmc.Anchor(
                    dmc.Button(
                        children=[
                            DashIconify(
                                icon="material-symbols:arrow-back-rounded",
                                width=20,
                                style={"marginRight": "5px"},
                            ),
                            "Back",
                        ],
                        variant="outline",
                        color="gray",
                        style={"width": "120px"},
                        loading=False,
                    ),
                    href=prev_href,
                ),
                width="auto",
            ),
            # Next button
            dbc.Col(
                dmc.Anchor(
                    dmc.Button(
                        children=[
                            "Next",
                            DashIconify(
                                icon="material-symbols:arrow-forward-rounded",
                                width=20,
                                style={"marginLeft": "5px"},
                            ),
                        ],
                        variant="outline",
                        color="gray",
                        style={"width": "120px"},
                        loading=False,
                    ),
                    href=next_href,
                ),
                width="auto",
            ),
        ],
        justify="between",
        align="center",
        style={"marginTop": "20px", "marginBottom": "20px", "padding": "0 20px"},
    )

    return nav_buttons
