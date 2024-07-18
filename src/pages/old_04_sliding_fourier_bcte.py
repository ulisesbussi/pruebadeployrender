# import dash_bootstrap_components as dbc
# from dash import dcc, html, register_page
# from dash_bootstrap_components import Col, Row
# import numpy as np

# from dash_bootstrap_templates import load_figure_template
# load_figure_template("slate")

# from utils import page as pgut
# from utils import pajama as utpj
# from utils import sliding as suut
# from pages.shared_pajama import shared_pajama

# #--------------------------------register-----------------------------
# register_page(__name__, path="/sliding-fourier-Bcte",
#               name = "Sliding Fourier constant B")
# #---------------------------------------------------------------------

# B,V,r = pgut.dd
# data = pgut.dd_data

# x_cte_data = {'x':V,'xname':'V','sec':B,'secname':'B'}

# #----------------------------------------------------------------
# #-------- buttons Col -----------------------------------------

# btn_fbackward = dbc.Button("", id="btn-faststepback",
#                             n_clicks=0, className="fa fa-fast-backward mr1")
# btn_backward = dbc.Button("", id="btn-stepback",
#                          n_clicks=0, className="fa fa-backward mr1")
# btn_forward = dbc.Button("", id="btn-stepforward",
#                          n_clicks=0, className="fa fa-forward mr1")
# btn_fforward = dbc.Button("", id="btn-faststepforward",
#                             n_clicks=0, className="fa fa-fast-forward mr1")
# btn_play = dbc.Button("", id="btn-play",
#                             n_clicks=0, className="fa fa-play mr1")
# btn_stop = dbc.Button("", id="btn-stop",
#                             n_clicks=0, className="fa fa-stop mr1")


# control_buttons = Col([btn_fbackward,btn_backward,
#                      btn_play,btn_stop,
#                      btn_forward,btn_fforward],width=4)


# inputs = Col([suut.get_inputs_and_texts(B,V,x_cte_data),])
# const_val_sel   = utpj.tryfloat(inputs.children[0].children[1].value)
# window_size_val = utpj.tryfloat(inputs.children[0].children[7].value)

# const_val_idx,window_size_idxs = suut.get_idx_const_ws(x_cte_data['sec'],
#                                                   x_cte_data['x'],
#                                                   const_val_sel,
#                                                   window_size_val)

# xy_di, selected_ranges = suut.get_xy_di(B,V,r,
#                                         const_val_idx,
#                                         x_cte_data['xname'],)


# fig = utpj.create_fig_and_cnf()
# fig = utpj.draw_Bcte_trace(fig, B,V,r)
# fig.data[0].update(xy_di)
# fig.add_vrect(x0=x_cte_data['x'][0], 
#               x1=x_cte_data['x'][window_size_idxs], 
#               line_width=0, 
#               fillcolor="red", 
#               opacity=0.2)
# fig.update_layout(
#     title="Plot Title",
#     xaxis_title=" V [mV]",
#     yaxis_title=r"&#916;G <sup> e<sup>2</sup></sup>/<sub>h</sub>")


# selected_ranges['const_val_idx']    = const_val_idx
# selected_ranges['window_size_idxs'] = window_size_idxs


# fwd = suut.get_windowed_fourier(xy_di,window_size_idxs)

# fig_freq = pgut.freq_graph(*suut.datadic_elem_to_arrdata(fwd['0']))
# fig_freq.update_xaxes(title_text="Freq [Hz]", row=2, col=1)
# fig_freq.update_yaxes(title_text="Amplitude", row=1, col=1)
# fig_freq.update_yaxes(title_text="Phase [rad]", row=2, col=1)


# #----------------------------------------------------------------
# #--------------------------layout--------------------------------
# #----------------------------------------------------------------

# layout = dbc.Container([
#     Row([
#         dcc.Store('x_cte_data-sliding', data= x_cte_data),
#         dcc.Store('curr-pos',data=0),
#         dcc.Store('curr-stepsize-bcte',data=1),

#         dcc.Store('fourier-windowed-data',data=fwd),
#         dcc.Store('ranges-sliding',data=selected_ranges),
#         dcc.Interval(id='interval-dv',interval=500,n_intervals=0),
#         Col([ inputs, 
#              control_buttons,
#              dcc.Graph(id='bcte-sliding', 
#                        figure=fig),
#              dcc.Graph(id='freq-sliding',
#                       figure=fig_freq),
#             ],width=6),

#     ]),
# ],className="h-100 mw-100 container-flex")


# # print(fig.data)
# # print(fig.)

# #%%
# # id_list = ['btn-faststepback','btn-stepback','btn-play','btn-stop',
# #            'btn-stepforward','btn-faststepforward',
# #            'x_cte_data-sliding','curr-pos','curr-stepsize-bcte',
# #            'fourier-windowed-data','ranges-sliding','interval-dv',
# #            'bcte-sliding','freq-sliding']