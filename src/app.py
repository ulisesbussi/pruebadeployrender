import dash_bootstrap_components as dbc
from dash import Dash


from utils.page import get_dataset, dd_data

from callbacks import (
        pajama_callbacks, 
        spectral_callbacks,
        plot3d_callbacks,
        sliding_callbacks,
        spectral_loaded_callbacks
        )
        
#from pages import plot3d_callbacks, pajama_callbacks

from dash_bootstrap_templates import load_figure_template
load_figure_template("slate")


FONT_AWESOME = (
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)

app = Dash(__name__,
           use_pages=True, 
           external_stylesheets=[dbc.themes.SLATE, '/assets/style.css',FONT_AWESOME],           
        )
#la app
#app._favicon = "favicon.ico",



from layout import get_layout  # esto tiene que ir si o si después de definir


data = dd_data

app.layout = get_layout(data)


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server('0.0.0.0', port=8050, debug=True,)
