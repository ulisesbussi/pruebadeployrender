# ## 03-aug-2023 Le dediqué 3.30 horas
# #todo list: fijarse como alinear las columnas y aumentar
# #tamaño de slider vertical
# #analizar la posibilidad de cortar con planos y no con lineas rectas


# from dash import (
#                 Dash, dcc, html, Input, 
#                 Output, State ,callback, ALL,
#                 register_page, Patch,
#                 ctx, no_update
#     )
# import dash_bootstrap_components as dbc
# import pandas as pd
# from plotly import graph_objs as go
# from dash_bootstrap_templates import load_figure_template
# import numpy as np
# load_figure_template("cyborg")


# from db_manipulation import utils as dbu

# #--------------------------------register-----------------------------
# register_page(__name__, path="/",name = "3D Plot")
# #---------------------------------------------------------------------


# import page_utils as pgut

# B,V,r = pgut.get_dataset()


# BB,VV,rr = B,V,r #sliced data
# #------------------------Funciones de figuras------------------------------


# #esto me define el orden de los traces

# fig, range_dic = pgut.create_fig_and_cnf(B,V,r)

# fig = pgut.surface_trace(    B, V, r, fig, range_dic     )
# fig = pgut.get_B_cte_traces( B, V, r, fig, range_dic, 763)
# fig = pgut.get_V_cte_traces( B, V, r, fig, range_dic, 173)
# fig = pgut.get_r_zqueeze(    B, V, r, fig, range_dic     )
# # [0] superficie
# #[ 1,2,3] B=cte
# #[4,5,6] V=cte
# #[7] R=cte


# def create_idx_slider(id,vec,n_marks=6,unit='',vertical=False):
#     "create idx slider"
#     n = len(vec)
#     st = n//n_marks
#     marks = { f"{i}": f"{vec[i]:.2f} {unit}" 
#              for i in range(0,n,st)}
#     if vertical:
#         verticalHeight = 700
#     else:
#         verticalHeight = 400
#     slider = dcc.Slider(id=f"slider-{id}",
#                         className=f"slider{id}",
#                         min=0,
#                         max=n-1,
#                         value=n//2,
#                         step=1,
#                         marks=marks,
#                         vertical=vertical,
#                         verticalHeight=verticalHeight,
#                         )
#     return slider

# def create_idx_rangeslider(id,vec,n_marks=6,unit='',vertical=False):
#     n = len(vec)
#     st = n//n_marks
#     marks = { f"{i}": f"{vec[i]:.2f} {unit}"
#              for i in range(0,n,st)}
#     if vertical:
#         verticalHeight = 700
#     else:
#         verticalHeight = 400
#     rgslider = dcc.RangeSlider(id=f"rgslider-{id}",
#                                className=f"rgslider{id}",
#                              min=0,
#                              max=n,
#                              value=[0,n],
#                              step=1,
#                              marks=marks,
#                              vertical=vertical,
#                              verticalHeight=verticalHeight,)
#     return rgslider

# layout = html.Div([
#     dcc.Store(id='data-store',data={}),
#     dbc.Col([
#         dbc.Row([
#             dbc.Col([create_idx_rangeslider("V", V,
#                                             unit="mV",
#                                             vertical=True
#                                             )
#                     ],
#                     className="el11",
#                     width=1,
#             ),
#             dbc.Col([create_idx_slider("V",V,
#                                        unit="mV",
#                                        vertical=True
#                                        )
#                     ],
#                     className="el12",
#                     width=1,
#             ),
#             dbc.Col([dcc.Graph(id="3d-graph", 
#                     figure=fig,className="fig3d",)],
#                     className="el13",
#                     width=5,
#             ),    
            
#             ],
#             #className="h-25",
#             style= {'height': '75vh'},
#         ),
#         dbc.Row(
#             dbc.Col([create_idx_slider("B",B,unit="T")],
#                 #className="row2",
#                 width=7),
#             ),
#         dbc.Row(
#             dbc.Col([create_idx_rangeslider("B",B,unit="T")],
#                 #className="row2",
#                 width=7),
#             ),
#         ],
#         className="col1",
#     )
        
        
# ])




# #------------------------Callbacks----------------------------------------

# #recordar dos callbacks no pueden afectar el mismo objeto..
# @callback(Output("3d-graph", "figure"),
#           Output("data-store", "data"),
#           [Input("slider-V", "value"),
#            Input("slider-B", "value"),
#            Input("rgslider-V", "value"),
#            Input("rgslider-B", "value"),
#            ],
#           [State("data-store", "data")]
#           )
# def update_vals(V_val,B_val,
#                 V_rang,B_rang,
#                 data):
#     # recupero los valores del estado. los mismos se almacenan
#     #como arrays de python y tengo que transformarlos en np.ndarrays
#     BB = np.array(data.get("B",B))
#     VV = np.array(data.get("V",V))
#     rr = np.array(data.get("r",r))
    
#     slider_changed = ctx.triggered_id
#     if slider_changed is None:
#         return no_update, {'B':BB,'V':VV,'r':rr}
#     patched_fig = Patch()


#     patched_fig, (BB,VV,rr) =pgut.update_surf_trace(B,V,r, 
#                                                         patched_fig, range_dic,
#                                                         V_se=V_rang, 
#                                                         B_se=B_rang)


#     V_val = min( max(V_val - V_rang[0],0), 
#                 V_rang[1]-V_rang[0]-1)
#     B_val = min( max(B_val - B_rang[0],0),
#                 B_rang[1]-B_rang[0]-1)
    
#     patched_fig = pgut.update_Vcte_val(BB,VV,rr,V_val,
#                                         patched_fig, 
#                                         range_dic)
#     patched_fig = pgut.update_Bcte_val(BB,VV,rr,B_val, 
#                                         patched_fig,
#                                         range_dic)
   
#     #     BB,VV,rr = slice_data(V_se=V_rang)
#     #     srf_vals = pgut.get_surf_vals(BB,VV,rr,range_dic)
#     #     patched_fig = pgut.update_surf_trace(srf_vals,patched_fig)
#     # if slider_changed == "rgslider-B":
#     #     BB,VV,rr = slice_data(B_se=B_rang)
#     #     srf_vals = pgut.get_surf_vals(BB,VV,rr,range_dic)
#     #     patched_fig = pgut.update_surf_trace(srf_vals,patched_fig)

#     return patched_fig, {'B':BB,'V':VV,'r':rr}



