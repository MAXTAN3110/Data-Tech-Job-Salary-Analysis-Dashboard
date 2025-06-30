import dash_bootstrap_components as dbc
from dash_iconify import DashIconify


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    DashIconify(
                        icon="mdi:home-outline", height=30, width=30, inline=True
                    ),
                    href="/",
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    DashIconify(
                        icon="mdi:briefcase-outline", height=30, width=30, inline=True
                    ),
                    href="/job-title",
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    DashIconify(
                        icon="mdi:map-marker-outline", height=30, width=30, inline=True
                    ),
                    href="/geo",
                )
            ),
            dbc.NavItem(
                dbc.NavLink(
                    DashIconify(
                        icon="mdi:office-building-outline",
                        height=30,
                        width=30,
                        inline=True,
                    ),
                    href="/company-size",
                )
            ),
        ],
        brand="Max Tan",
        brand_href="/",
        color="#41C9EA",
        dark=True,
    )
    return navbar
