from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import base64


#automatic all children
children_pages=[
    *[
    dbc.NavItem(dbc.NavLink(page["name"], 
        href=page["path"]),)
            for page in dash.page_registry.values() 
                if page["module"] != "pages.not_found_404" 
    ],   
]
# #print(children_pages)

#grouped children
children_groups=[
    
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("3D Plot",            href="/"),
            dbc.DropdownMenuItem("V-constant Fourier", href="/vcte-fourier"),
            dbc.DropdownMenuItem("B-constant Fourier", href="/bcte-fourier"),
            dbc.DropdownMenuItem("Sliding Fourier B-constant", href="/sliding-fourier-Bcte"),
            dbc.DropdownMenuItem("Sliding Fourier V-constant", href="/sliding-fourier-Vcte"),
        ],
        nav=True,
        in_navbar=True,
        label="Nakamura's Data",),
    dbc.DropdownMenu(
        children=[
            dbc.DropdownMenuItem("Fourier ", href="/load_fourier"),
        ],
        nav=True,
        in_navbar=True,
        label="Uploaded Data",),
]
        

svg_file = 'assets/Nokia_Bell_Labs_2023.svg'
encoded = base64.b64encode(open(svg_file,'rb').read()) 
svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode()) 
html_img = html.Img(src=svg,
                    height=40,className="ms-2")


NameLogo = dbc.Container([
            html.A(
                dbc.Row([
                        dbc.Col(html_img),
                        dbc.Col(dbc.NavbarBrand("Data & Devices Visual Lab", className="ms-2")),
                        ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),

        ],
        className="ms-0" 
    ),



def get_navbar():
    nv = dbc.NavbarSimple(id = "navbar",
            children = children_groups,#children_pages,#children_fixed,
            brand=NameLogo,#'Data&Devices Visual Lab',
            #brand_href='assets/dash_logo.png', #link a algo?
            
            className="fs-20",#"navbar",
            color='secondary',
            dark=True,
            style={"margin": False}  ,
        )
    return nv

def get_layout(dat={}):
    

    layout = dbc.Container([
        get_navbar(),
        dash.dcc.Store(id='shared-data', data=dat),    
        dash.page_container,
        
    ],className="mw-100 container-flex")
    return layout