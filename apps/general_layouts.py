import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Market Overview", href='/apps/mkt_overview')),
        dbc.NavItem(dbc.NavLink("Custom Search", href='/apps/custom_search')),
    ],
    brand="πlitica: Equity Analysis",
    brand_href="#",
    color="primary",
    dark=True,
)