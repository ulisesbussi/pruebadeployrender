from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input,Output,Patch,State

from pages import pajama_callbacks
from page_utils import get_dataset

app = Dash(__name__,
           use_pages=True, 
           external_stylesheets=[dbc.themes.SLATE, '/assets/style.css'],
           
           #suppress_callback_exceptions=True)
        )
server = app.server
from layout import get_layout #esto tiene que ir si o si después de definir
#la app

# print("""
#       TODO: 
#       1-tengo que conservar los valores de pajama entre páginas
#       probablemente un state para pasarlos
#       2- tengo que modificar el callback en la segunda pagina
#       para que el pajama modifique el plot
#       3- ver la posibilidad de interactuar con el gráfico para 
#       seleccionar componentes de fourier a graficar.


B,V,r = get_dataset()
dat ={'B':B.tolist(),'V':V.tolist(),'r':r.tolist()}

app.layout = get_layout(dat)


if __name__ == '__main__':
    app.run_server(debug=True,)
#    app.run_server(host= '0.0.0.0',port=8080,debug=True,)




# @app.callback(Output('shared-data', 'data'),
#               Input('navbar', 'activeNavItem')
#             )
# def load_data( active_page):
#     B,V,r = get_dataset()
#     # shared_patch = Patch
#     # shared_patch['B'] = B.tolist()
#     # shared_patch['V'] = V.tolist()
#     # shared_patch['r'] = r.tolist()
#     # return shared_patch
#     return {'B':B.tolist(),'V':V.tolist(),'r':r.tolist()}
    