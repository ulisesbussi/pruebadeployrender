## 03-aug-2023 Le dediqué 3.30 horas
#todo list: fijarse como alinear las columnas y aumentar
#tamaño de slider vertical
#analizar la posibilidad de cortar con planos y no con lineas rectas
## 04-aug-2023 Le dediqué 4.30 horas

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
import numpy as np
load_figure_template("cyborg")

import json


#from db_manipulation import utils as dbu

#--------------------------------register-----------------------------
register_page(__name__, path="/",name = "3D Plot")
#---------------------------------------------------------------------


import page_utils as pgut
import utils_pajama as utpj
B,V,r = pgut.get_dataset()

#------------------------Funciones de figuras------------------------------
f_img = utpj.create_fig_and_cnf()
f_img = utpj.draw_img_trace(f_img,B,V,r)

f_v = utpj.create_fig_and_cnf()
f_v = utpj.draw_Vcte_trace(f_v,B,V,r)


f_b = utpj.create_fig_and_cnf()
f_b = utpj.draw_Bcte_trace(f_b,B,V,r)


#esto me define el orden de los traces

fig, fig_range_dic = pgut.create_fig_and_cnf(B,V,r)

fig = pgut.surface_trace(    B, V, r, fig, fig_range_dic  )
fig = pgut.get_B_cte_traces( B, V, r, fig, fig_range_dic  )
fig = pgut.get_V_cte_traces( B, V, r, fig, fig_range_dic  )
fig = pgut.get_r_zqueeze(    B, V, r, fig, fig_range_dic  )
# [0] superficie
#[ 1,2,3] B=cte
#[4,5,6] V=cte
#[7] R=cte

def correct_vert_slider_vals(vals,maxVal):
    vals = [maxVal-i-1 for i in vals][::-1]
    return vals


def create_idx_rangeslider(id,vec,n_marks=6,unit='',
                           vertical=False,reversed=False):
    n = len(vec)
    st = n//n_marks

    marks = { f"{i}": f"{vec[i]:.2f} {unit}"
        for i in range(0,n,st)}
    min_val = 0
    max_val = n-1
  
   
    # if reversed:
    #     marks = { f"{n-i-1}": f"{vec[i]:.2f} {unit}"
    #              for i in range(0,n,st)}
    
    
   
    rgslider = dcc.RangeSlider(id=f"rgslider-{id}",
                               className=f"rgslider{id}",
                             min=min_val,
                             max=max_val,
                             value=[min_val,n//2,max_val    ],
                             step=1,
                             marks=marks,
                             vertical=vertical,

                             )
    return rgslider


from pages.shared_pajama import shared_pajama


#------------------------Layout----------------------------------------
layout = dbc.Container([#html.Div([
  Row([
    #la primer columna va a tener el plot de antes
    Col([ #la primer fila en esta col tiene el slider y el plot
      Row([ 
        dbc.Col([create_idx_rangeslider("V", V, unit="mV",vertical=True)
            ],width=1, className='vert-slide-col' ),
        dbc.Col([dcc.Graph(id="3d-graph", figure=fig,className="fig3d",)
            ],width=11,),  
      ],className="row1-3d"),  
      html.Br(),
      Row([
        dbc.Col([create_idx_rangeslider("B",B,unit="T")], width=12),
      ]),
    ], className="col50width"),
    
    #----------------- Segunda columna----------------------------
    # , 
    shared_pajama,
  ]),
],className="container-flex" ) #,style= {'height': '75vh','width':'100%'},)
  















# OLD layout 
# layout = html.Div([
#     #dcc.Store(id='data-store-3d',data={}),
#     dbc.Col([
#         dbc.Row([
#             dbc.Col([create_idx_rangeslider("V", V, unit="mV",vertical=True)
#                     ],className="el11", width=1, ),
#             dbc.Col([dcc.Graph(id="3d-graph", figure=fig,className="fig3d",)
#                      ],className="el13", width=5,),    
#             ],style= {'height': '75vh'}, ),
#         dbc.Row(
#             dbc.Col([create_idx_rangeslider("B",B,unit="T")], width=6),
#             ),
#         dbc.Row(
#             dbc.Col(dbc.Button("Save",id="save-bnt",n_clicks=0),),
#             ),
#         ], className="col1",  width=6,  
#     ),
#     #comienzo la parte derecha
        
# ])




#------------------------Callbacks----------------------------------------

#recordar dos callbacks no pueden afectar el mismo objeto..
@callback([Output("3d-graph", "figure"),
          Output("shared-data", "data")],
          [Input("rgslider-V", "value"),
           Input("rgslider-B", "value"),
           ],
          State("shared-data", "data")
          )
def update_vals(V_rang, B_rang, data):

    B,V,r = pgut.get_dataset()
    
    
    data_patch = Patch()
    if data.get('B') is None:
        data_patch['B'] = B.tolist()
        data_patch['V'] = V.tolist()
        data_patch['r'] = r.tolist()

    slider_changed = ctx.triggered_id
    if slider_changed is None:
        return no_update,  data_patch
    
    data_patch['B_rang'] = B_rang
    data_patch['V_rang'] = V_rang
    

    patched_fig = Patch()
    #update surface_plot
    patched_fig = pgut.update_surf_trace(B,V,r, 
                                        patched_fig, 
                                        B_rang,
                                        V_rang,
                                        fig_range_dic)
    
    #update B=cte and V=cte traces
    patched_fig = pgut.update_Bcte_val(B,V,r, 
                                       patched_fig,
                                       B_rang,V_rang,
                                       fig_range_dic)
    patched_fig = pgut.update_Vcte_val(B,V,r, 
                                       patched_fig,
                                       B_rang,V_rang,
                                       fig_range_dic)
   
    patched_fig = pgut.update_squeeze_val(B,V,r,
                                          patched_fig,
                                          B_rang,V_rang,
                                          fig_range_dic)


    
    return patched_fig,data_patch



