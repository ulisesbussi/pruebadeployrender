
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
import json

import utils_pajama as utpj

#%%


import page_utils as pgut
B,V,r = pgut.get_dataset()


f_img = utpj.create_fig_and_cnf()
f_img = utpj.draw_img_trace(f_img,B,V,r)

f_v = utpj.create_fig_and_cnf()
f_v = utpj.draw_Vcte_trace(f_v,B,V,r)


f_b = utpj.create_fig_and_cnf()
f_b = utpj.draw_Bcte_trace(f_b,B,V,r)

#%%


def create_idx_rangeslider(id,vec,n_marks=6,unit='',vertical=False, 
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
                             value=[0,n//2,n-1    ],
                             step=1,
                             marks=marks,
                             vertical=vertical,
                             )
    return rgslider

#%%

#----------------- Segunda columna----------------------------
shared_pajama =  Col([ #la segunda columna va a tener la parte de varios graficos
      Row([ #fila 1 : slider-plot || txt-inp
        Col([
          create_idx_rangeslider("b-pajama-3dplot",B,unit="T",vertical=False),
          dcc.Graph(id="vcte-pajama-3dplot", figure=f_v,className="pajama-short-fig"), 
        ], width=8),
        Col([ #este col bloque txt y 2 inp en misma fila
            Row([
              html.P("B range (min,max) [T]"),
              Col([
                dbc.Input(id="Bmin-3dplot", # type="number",
                           value=f"{B.min():.2f} ",#Bmin es el minimo de B o sea B[-1]
                          className="pajama-input"),   
              ], width=6),
              Col([
                dbc.Input(id="Bmax-3dplot", #type="number",
                           value=f"{B.max():.2f}",
                          className="pajama-input"),
              ], width=6),
            ]), 
            Row([
              html.P("V range (min,max) [mV]"),
              Col([
                dbc.Input(id="Vmin-3dplot", # type="number",
                           value=f"{V.min():.2f}",
                          className="pajama-input"),   
              ], width=6),
              Col([
                dbc.Input(id="Vmax-3dplot", #type="number",
                           value=f"{V.max():.2f}",
                          className="pajama-input"),
              ], width=6),
            ]),  
        ], width=4),  
      ], className="pajama-row1"),  
      html.Br(), 
      Row([ #fila 2 de la parte derecha : imagen || plot-slider
        Col([# f2 col1: imagen
          dcc.Graph(id="img-graph-3dplot", figure=f_img,),
        ],width=8),
        Col([# f2 col2: plot-slider
          Row([
            Col([ 
                dcc.Graph(id="bcte-pajama-3dplot", figure=f_b,className="pajama-narrow-fig"),
            ],width=9),
            Col([  
                create_idx_rangeslider("v-pajama-3dplot",V,unit="nm",vertical=True),
            ],width=3),
          ]),
        ],width=4),
      ], className="pajama-row2"),
    ], className="col50width")


#%%




# @callback(Output("rgslider-b-pajama-3dplot", "value"),
#            Output("vcte-pajama-3dplot", "figure"),
#            Output("Bmin-3dplot", "value"),
#            Output("Bmax-3dplot", "value"),
#            Output("Vmin-3dplot", "value"),
#            Output("Vmax-3dplot", "value"),
#            Output("img-graph-3dplot", "figure"),
#            Output("bcte-pajama-3dplot", "figure"),
#            Output("rgslider-v-pajama-3dplot", "value"),
#           [Input("rgslider-b-pajama-3dplot", "value"),
#            Input("rgslider-v-pajama-3dplot", "value"),
#            Input("Bmin-3dplot", "value"),
#            Input("Bmax-3dplot", "value"),
#            Input("Vmin-3dplot", "value"),
#            Input("Vmax-3dplot", "value"),],
#            State("shared-data", "data"),
#           )
# def update_pajama(B_rang,V_rang,bm,bM,vm,vM,data):
#     event = ctx.triggered_id
#     print(event)
#     if event is None:
#         return no_update,no_update,no_update,\
#                 no_update,no_update,no_update,\
#                 no_update,no_update,no_update
        
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
#     if event == "rgslider-b-pajama-3dplot":
#         #change bm and bM
#         bM = f"{B[B_rang[0]]:.2f}" #aca el 0 es el max
#         bm = f"{B[B_rang[2]]:.2f}" #aca el 2 es el min
#     if event == "rgslider-v-pajama-3dplot":
#         #change vm and vM
#         vm = f"{V[V_rang[0]]:.2f}" #aca el 0 es el min
#         vM = f"{V[V_rang[2]]:.2f}" #aca el 2 es el max
    
#     if event in ["Bmin-3dplot","Bmax-3dplot"]:
#         #change B_rang finding nearest indices
#         bM = utpj.tryfloat(bM)
#         bm = utpj.tryfloat(bm)
#         if not (bM is None or bm is None):
#             ibM = np.argmin(np.abs(B-bM))
#             ibm = np.argmin(np.abs(B-bm))
#             #check if B_rang[1] is in limits if no replace for nearest
#             B_rang[0] = ibM
#             B_rang[2] = ibm
#             if ibM < B_rang[1]:
#                 B_rang[1] = ibM
#             if ibm > B_rang[1]:
#                 B_rang[1] = ibm
#     if event in ["Vmin-3dplot","Vmax-3dplot"]:
#         #change V_rang finding nearest indices
#         vM = utpj.tryfloat(vM)
#         vm = utpj.tryfloat(vm)
#         if not (vM is None or vm is None):
#             ivM = np.argmin(np.abs(V-vM))
#             ivm = np.argmin(np.abs(V-vm))
#             #check if V_rang[1] is in limits if no replace for nearest
#             V_rang[0] = ivm
#             V_rang[2] = ivM
#             if ivM < V_rang[1]:
#                 V_rang[1] = ivM
#             if ivm > V_rang[1]:
#                 V_rang[1] = ivm
        
#     #update figs
#     bcte_dic = utpj.update_Bcte_val(B,V,r,B_rang,V_rang)
#     vcte_dic = utpj.update_Vcte_val(B,V,r,B_rang,V_rang)
#     img_dic  = utpj.update_img_val(B,V,r,B_rang,V_rang)
#     patched_bcte = Patch()
#     patched_vcte = Patch()
#     patched_img  = Patch()
#     patched_bcte = utpj.update_Bcte_trace(patched_bcte,bcte_dic)
#     patched_vcte = utpj.update_Vcte_trace(patched_vcte,vcte_dic)
#     patched_img  = utpj.update_img_trace(patched_img,img_dic)
    
#     print(B_rang)
#     return B_rang, patched_vcte, bm, bM, \
#             vm, vM, patched_img, patched_bcte, V_rang
 