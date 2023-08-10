# ## 03-aug-2023 Le dediqué 3.30 horas
# #todo list: fijarse como alinear las columnas y aumentar
# #tamaño de slider vertical
# #analizar la posibilidad de cortar con planos y no con lineas rectas


# from dash import (
#                 Dash, dcc, html, Input, 
#                 Output, State ,callback, ALL,
#                 register_page, Patch,
#                 ctx
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

# # def get_fig_ranges(B,V,r,k=0.3,B_se=[0,-1],
# #                    V_se=[0,-1]):
# #     """calcula los limites de la imagen y los devuelve"""
# #     B = B[B_se[0]:B_se[1]]
# #     V = V[V_se[0]:V_se[1]]
# #     r = r[V_se[0]:V_se[1],B_se[0]:B_se[1]]
# #     min_x,max_x = B.min(),B.max()
# #     min_y,max_y = V.min(),V.max()
# #     min_z,max_z = r.min(),r.max()
# #     range_x = [min_x - k*(max_x - min_x), max_x + k*(max_x - min_x)]
# #     range_y = [min_y - k*(max_y - min_y), max_y + k*(max_y - min_y)]
# #     range_z = [min_z - k*(max_z - min_z), max_z + k*(max_z - min_z)]
# #     return range_x,range_y,range_z


# def slice_data(B_se=None,V_se=None):
#     if B_se is None:
#         B_se = [0,-1]
#     if V_se is None:
#         V_se = [0,-1]
#     global BB,VV,rr
#     BB = B[B_se[0]:B_se[1]]
#     VV = V[V_se[0]:V_se[1]]
#     rr = r[V_se[0]:V_se[1],B_se[0]:B_se[1]]
    
    
    
# # def create_fig_and_cnf(B,V,r):
# #     "crea la figura y setea los límites de la misma"
# #     range_x, range_y, range_z = get_fig_ranges(B,V,r)
    
# #     fig = go.Figure()
# #     fig.update_layout(
# #         autosize = False,
  
# #         scene = dict(
# #             xaxis = page_utils.scene_axis_dict(range_x),
# #             yaxis = page_utils.scene_axis_dict(range_y, 
# #                                               "rgb(230, 200,230)"),
# #             zaxis = page_utils.scene_axis_dict(range_z,
# #                                               "rgb(30, 230,200)"),
# #             xaxis_title='B [T]',
# #             yaxis_title='V [mV]',
            
# #         ),        
# #         margin=dict(
# #             r=10,l=10,
# #             b=10,t=10),
# #         height = 700,
# #         legend=dict(orientation='h',yanchor='bottom',
# #                     xanchor='center',y=1,x=0.5)
# #         #width = 1000,
# #         #showlegend = False,

# #     )
    
# #     return fig ,{'x':range_x,'y':range_y,'z':range_z}
    
            


# # def surface_trace(fig,B,V,r,ranges):
# #     """Genera la superficie para el plot"""
# #     fig.add_surface(x=B, y=V, z=r,
# #                     colorscale='jet',
# #                     name = 'surface',
# #                     colorbar=dict(
# #                         title="\delta G \[e^2/h\]",
# #                         lenmode='fraction',
# #                         len=0.7,
# #                         ),              
# #     )
# #     return fig



# # def get_dics_val_b_cte(B,V,r,idx,ranges):
# #     vals = r[:,idx]
# #     onvl = np.ones_like(vals)
# #     wall = {'x':ranges['x'][0]* onvl,
# #             'y':V,
# #             'z':vals}
# #     surf = {'x':B[idx]*onvl,
# #             'y':V,
# #             'z':vals}
# #     floor = {'x':B[idx]*onvl,
# #              'y':V,
# #              'z':ranges['z'][0]*onvl}
# #     return wall,surf,floor

# # def get_dics_val_v_cte(B,V,r,idx,ranges):
# #     vals = r[idx,:]
# #     onvl = np.ones_like(vals)
# #     wall = {'x':B,
# #             'y':ranges['y'][0]* onvl,
# #             'z':vals}
# #     surf = {'x':B,
# #             'y':V[idx]*onvl,
# #             'z':vals}
# #     floor = {'x':B,
# #              'y':V[idx]*onvl,
# #              'z':ranges['z'][0]*onvl}
# #     return wall,surf,floor

# # def get_squeeze_vals(B,V,r,ranges):
# #     di = {'x':B,'y':V,
# #           'z':ranges['z'][0]*np.ones_like(r)}
# #     return di

# # def get_surf_vals(B,V,r,ranges):
# #     di = {'x':B,'y':V,'z':r}
# #     return di


# # def get_B_cte_traces(fig,B,V,r, idx, ranges):
# #     """crea las 3 trazas relacionadas a B=cte"""
    
# #     dic_list = get_dics_val_b_cte(B,V,r,idx,ranges)
# #     names = ['B proy','B surf','B floor']
# #     for di,name in zip(dic_list,names):
# #         fig.add_trace(go.Scatter3d(**di,
# #                                    mode='lines',
# #                                    name=name))
# #         fig.data[-1].update(line=dict(color='black', width=10))
# #     return fig


# # def get_V_cte_traces(B,V,r, idx, ranges):
# #     """crea las 3 trazas relacionadas a V=cte"""
# #     dic_list = get_dics_val_v_cte(B,V,r,idx,ranges)
# #     names = ['V proy','V surf','V floor']
# #     for di,name in zip(dic_list,names):
# #         fig.add_trace(go.Scatter3d(**di,
# #                                    mode='lines',
# #                                    name=name))
# #         fig.data[-1].update(line=dict(color='black', width=10))
# #     return fig


# # def get_r_zqueeze(fig,B,V,r, ranges):
# #     """crea las sombra de R como imagen en el piso"""
# #     di = get_squeeze_vals(B,V,r,ranges)
# #     fig.add_trace(go.Surface(**di,
# #                              surfacecolor=r,
# #                              cmin=r.min(),
# #                              cmax=r.max(),
# #                              colorscale='jet',
# #                              showscale=False,
# #                 )
# #     )
# #     return fig


    
    
# #esto me define el orden de los traces

# fig,range_dic = pgut.create_fig_and_cnf(B,V,r)
# fig = pgut.surface_trace(fig,B,V,r,range_dic)
# fig = pgut.get_B_cte_traces(fig,B,V,r, 763, range_dic)
# fig = pgut.get_V_cte_traces(B,V,r, 173, range_dic)
# fig = pgut.get_r_zqueeze(fig,B,V,r, range_dic)
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

# # def update_Vcte_val(v_val, patched_fig):

# #     traces_v_dic = get_dics_val_v_cte(B,V,r,v_val,range_dic)
# #     traces_indices = [4,5,6]
# #     for tr_di,trace_index in zip(traces_v_dic,traces_indices):
# #         patched_fig.data[trace_index].update(tr_di)
# #     return patched_fig

# # def update_Bcte_val(b_bal, patched_fig):
# #     traces_b_dic = get_dics_val_b_cte(B,V,r,b_bal,range_dic)
# #     traces_indices = [1,2,3]
# #     for tr_di,trace_index in zip(traces_b_dic,traces_indices):
# #         patched_fig.data[trace_index].update(tr_di)
# #     return patched_fig

# # def update_surf_trace(srf_vals,patched_fig):
# #     patched_fig.data[0].update(srf_vals)
# #     return patched_fig


# #recordar dos callbacks no pueden afectar el mismo objeto..
# @callback(Output("3d-graph", "figure"),
#           [Input("slider-V", "value"),
#            Input("slider-B", "value"),
#            Input("rgslider-V", "value"),
#            Input("rgslider-B", "value"),
#            ]
#           )
# def update_vals(V_val,B_val,V_rang,B_rang):
#     slider_changed = ctx.triggered_id
    
#     patched_fig = Patch()
#     if slider_changed == "slider-V":
#         patched_fig = pgut.update_Vcte_val(V_val,patched_fig,
#                                            BB,VV,rr,range_dic)
#     if slider_changed == "slider-B":  
#         patched_fig = pgut.update_Bcte_val(B_val,patched_fig)
#     if slider_changed == "rgslider-V":
#         slice_data(V_se=V_rang)
#         srf_vals = pgut.get_surf_vals(BB,VV,rr,range_dic)
#         patched_fig = pgut.update_surf_trace(srf_vals,patched_fig)
#     if slider_changed == "rgslider-B":
#         slice_data(B_se=B_rang)
#         srf_vals = pgut.get_surf_vals(BB,VV,rr,range_dic)
#         patched_fig = pgut.update_surf_trace(srf_vals,patched_fig)

#     return patched_fig



