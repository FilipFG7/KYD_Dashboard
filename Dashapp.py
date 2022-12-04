# importing the libraries
import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd   
import dash_labs as dl

# app creation in dash
app= dash.Dash(__name__, plugins=[dl.plugins.pages],external_stylesheets=[dbc.themes.LUX])

# creating a dropdown for the pages
dropdown=dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem(page["name"], href=page["path"])
                    for page in dash.page_registry.values()
                    if page["module"] != "pages.not_found_404"
                ],
                nav=True,
                label="More pages",
                in_navbar=True,                
            )
# creating a responsive header for the webapp
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [                          
                        dbc.Col(dbc.NavbarBrand("Data visualization", className="ms-2", style={'fontSize':'200%', 'fontColor':'#F2F2F2'})),                        
                    ],
                    align="center",
                    className="g-0",                   
                ),               
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
            # insert a dropdown into navbar
            dbc.Collapse(
                dbc.Nav(
                    [dropdown],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ],
    ),
    color="#262626",
    dark=True,
    className="mb-5",    
)
# giving the app a layout - resposive header and page contents
app.layout = dbc.Container(
    [navbar, dl.plugins.page_container],
    fluid=True,
)
        
# running webapp
if __name__ == '__main__':
    app.run_server(debug=True)
