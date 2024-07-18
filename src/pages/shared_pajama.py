
from dash import (
                Dash, dcc, html, Input, 
                Output, State ,callback, ALL,
                register_page, Patch,
                ctx, no_update
    )
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_components import Col, Row
import pandas as pd
from plotly import graph_objs as go

from dash_bootstrap_templates import load_figure_template
load_figure_template("slate")

import numpy as np
import json



#import utils_pajama as utpj
from utils import pajama as utpj

#%%



from utils import page as pgut


B,V,r = pgut.dd
data = pgut.dd_data

f_img = utpj.create_fig_and_cnf()
f_img = utpj.draw_img_trace(f_img,B,V,r)

f_v = utpj.create_fig_and_cnf()
f_v = utpj.draw_Vcte_trace(f_v,B,V,r)


f_b = utpj.create_fig_and_cnf()
f_b = utpj.draw_Bcte_trace(f_b,B,V,r)

#%%


def create_idx_rangeslider(id,vec,n_marks=6,
                           unit='',vertical=False, 
                           ):
    n = len(vec)
    st = n//n_marks
    marks = { f"{i}": f"{vec[i]:.2f} {unit}"
        for i in range(0,n,st)}
    min_val = 0
    max_val = n-1
    rgslider = dcc.RangeSlider(id=f"rgslider-{id}",
                               className=f"rgslider{id}",
                             min=min_val,
                             max=max_val,
                             value=[min_val,n//2,max_val],
                             step=1,
                             marks=marks,
                             vertical=vertical,
                             persistence=True, persistence_type='memory'
                             )
    return rgslider
#%% elemenmts in layout


rg_b_pajama = create_idx_rangeslider("b-pajama",B,unit="T",vertical=False)
vcte_pajama = dcc.Graph(id="vcte-pajama", figure=f_v,className="pajama-short-fig")


#persistence is not working for inputs and sliders
# it's seems it's a problem with the callbacks
inp_Bmin = dbc.Input(id="Bmin",
                    value=f"{B.min():.4f} ",#Bmin es el minimo de B o sea B[-1]
                    className="pajama-input",
                    #persistence=True, persistence_type='memory',
                    debounce=True)
inp_Bmax = dbc.Input(id="Bmax", 
                    value=f"{B.max():.4f}",
                    className="pajama-input",
                    debounce=True)
inp_Bsel = dbc.Input(id="Bsel",
                    value=f"{B.mean():.4f}",
                    className="pajama-input",
                    debounce=True)

inp_B = dbc.InputGroup([ inp_Bmin, inp_Bsel, inp_Bmax ])


inp_Vmin = dbc.Input(id="Vmin",
                    value=f"{V.min():.2f} ",#Bmin es el minimo de B o sea B[-1]
                    className="pajama-input",
                    debounce=True)
inp_Vmax = dbc.Input(id="Vmax",
                    value=f"{V.max():.2f}",
                    className="pajama-input",
                    debounce=True)
inp_Vsel = dbc.Input(id="Vsel",
                    value=f"{ V.mean():.2f}",
                    className="pajama-input",
                    debounce=True)

inp_V = dbc.InputGroup([ inp_Vmin, inp_Vsel, inp_Vmax ])

img_pajama = dcc.Graph(id="img-graph", figure=f_img,className="m-0")


rg_v_pajama = create_idx_rangeslider("v-pajama",V,unit="mV",vertical=True)
bcte_pajama = dcc.Graph(id="bcte-pajama", figure=f_b,className="pajama-narrow-fig")


btn_tr_vcte = dbc.Button(" Download V-trace", 
                         id ="btn-dwnld-vcte",
                         n_clicks=0,className='fa fa-download mr-1')
    
btn_tr_bcte = dbc.Button(" Download B-trace",
                         id ="btn-dwnld-bcte",
                         n_clicks=0,className='fa fa-download mr-1')

btn_img = dbc.Button(" Download image",
                        id ="btn-dwnld-img",
                        n_clicks=0,className='fa fa-download mr-1')


# vamos a dividir el layout del pajama en un 2x2, es una columna c/2 filas
# la primera fila tiene 2 cols: slider_plot || txtInp
# la segunda fila tiene 2 cols: image || plot_slider

slider_plot = Col([ rg_b_pajama,
                    vcte_pajama,
                ], width = 8, className="m-0")


txtInp = Col([ #este col bloque txt y 2 inp en misma fila
            Row([ html.P("B range (min,sel,max) [T]")], className="m-0"),

            # Row([Col([inp_Bmin], width=4, className="m-0"), 
            #      Col([inp_Bsel], width=4, className="m-0"),
            #      Col([inp_Bmax], width=4, className="m-0"),
            #      ],className="m-0"),
            Row([ inp_B], className="m-0"),
            Row([ html.P("V range (min,sel,max) [mV]")], className="m-0"),

            Row([ inp_V], className="m-0"),
            # Row([Col([inp_Vmin], width=4, className="m-0"),
            #     Col([inp_Vsel], width=4, className="m-0"),
            #     Col([inp_Vmax], width=4, className="m-0"),
            #     ],className="m-0"),
            
        ], width=4)


image = Col([img_pajama], width=8, className="m-0")

plot_slider = Col([
                Row([
                    Col([bcte_pajama,],width=10, className="m-0"),
                    Col([rg_v_pajama,], width=2, className="m-0")],
                className="m-0")
               ],width=3)


btns = Col([btn_tr_vcte,
            btn_tr_bcte,
            btn_img], width=12, className="m-0")

#%%

#----------------- Columna de pajama----------------------------
shared_pajama =  Col([ #la segunda columna va a tener la parte de varios graficos
      Row([ #fila 1 : slider-plot || txt-inp
        slider_plot,
        txtInp,      ], className="h-20"),#pajama-row1"),  
      html.Br(), 
      Row([ #fila 2 de la parte derecha : imagen || plot-slider
        image,
        plot_slider,      ], className="h-80"),#"pajama-row2"),
      Row([ btns], className="h-10"),
      dcc.Download(id='Download'),#"pajama-row3"),
    ], className="w-50 h-100 ms-0 me-10")#"col50width")


#%%


