from dash import (
                    Output, Input, State, 
                    callback,no_update,Patch,ctx
                )
import numpy as np

from utils import page as pgut
from utils import pajama as utpj
from utils import sliding as suut


#------------------- Calbacks used to Bcte ------------------------------


# @callback(Output('bcte-sliding', 'figure'),
#           Output('freq-sliding', 'figure'),
#           Output('btn-play','className'),
          
#           Input('curr-pos', 'data'),
          
#           State('shared-data', 'data'),
#           State('fourier-windowed-data','data'),
#           State('Bsel-sliding','value'),
#           State('delta-V-sliding','value'),
#           State('ranges-sliding','data'),
#           State('x_cte_data-sliding','data'),
#           prevent_initial_call=True)
# def update_window(curr_pos,
#                   data,fwd,
#                   const_val_sel,window_size_val,
#                   ranges,x_cte_data):
    
#     x_cte_data = suut.to_np_arrays_in_dic(x_cte_data)
    
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
#     window_size_val = utpj.tryfloat(window_size_val)
#     const_val_sel = ranges['V_rang'][1] #ranges['B_rang'][1]
#     const_val_idx,window_size_idxs = suut.get_idx_const_ws(x_cte_data['sec'],
#                                                       x_cte_data['x'],
#                                                       const_val_sel,
#                                                       window_size_val)
    
#     xy_di,_ = suut.get_xy_di(B,V,r,const_val_idx,x_cte_data['xname'],
#                         ranges['B_rang'],ranges['V_rang'])
    
#     fig_rec  = Patch()
#     fig_freq = Patch()
#     fig_rec.layout.shapes[0].update(x0=xy_di['x'][curr_pos],
#                                 x1=xy_di['x'][curr_pos+window_size_idxs])
    
#     freq,signal_f = suut.datadic_elem_to_arrdata(fwd[str(curr_pos)])
#     fig_freq.data[0].update(x=freq,
#                             y=np.abs(signal_f))
#     fig_freq.data[1].update(x=freq,
#                             y=np.angle(signal_f))
    
#     return fig_rec,fig_freq,'fa fa-pause mr1'


# @callback(Output('curr-pos', 'data',      allow_duplicate=True),
#           Output('btn-play', 'className', allow_duplicate=True),
#           Output('btn-play', 'n_clicks',  allow_duplicate=True),
          
#           Input('btn-stop',             'n_clicks'),
#           Input('btn-faststepback',     'n_clicks'),
#           Input('btn-stepback',         'n_clicks'),
#           Input('btn-play',             'n_clicks'),
#           Input('btn-stepforward',      'n_clicks'),
#           Input('btn-faststepforward',  'n_clicks'),
#           Input('interval-dv',          'n_intervals'),
#           Input('fourier-windowed-data','data'),
          
#           State('curr-pos',         'data'),
#           State('curr-stepsize-bcte',   'data'),
#           prevent_initial_call=True)
# def update_curr_pos(bt_stop,bt_fback,bt_back, bt_play,
#                     bt_for,bt_ffor,interval,fwd,curr_pos,curr_step):
#     max_n = np.array(list(fwd.keys()),dtype=int).max()
    
#     trigger_el = ctx.triggered_id
#     if trigger_el == 'fourier-windowed-data':
#         return 0,'fa fa-play mr1',0
    
#     if trigger_el=='btn-play':#prioridad en play cambio esado de play
#         state = 'fa fa-pause mr1' if bt_play%2 else 'fa fa-play mr1'
#         return no_update,state,bt_play#bt_play cambia solo
    
#     if trigger_el=='btn-stop':#prioridad en stop
#         return 0,'fa fa-play mr1',0
    
#     if trigger_el=='interval-dv' and bt_play%2:
#         curr_pos = curr_pos + curr_step #avanzo
    
    
#     el_di = {'btn-faststepback':   -5*curr_step,
#              'btn-stepback':       -1*curr_step,
#              'btn-stepforward':     1*curr_step,
#              'btn-faststepforward': 5*curr_step,
#              'interval-dv':         0}#ya avancé arriba si está en play
    
#     curr_pos = curr_pos + el_di[trigger_el] #incremento curr_pos
    
#     if curr_pos > max_n: #termine no actualizo la posición y cambio a play
#         return no_update, 'fa fa-play mr1', 0
#     if curr_pos < 0: #retrocedí demasiado pos a 0
#         return 0, no_update,no_update
    
#     return curr_pos,no_update,no_update


# @callback(Output('fourier-windowed-data','data'),
#           Output('bcte-sliding','figure',allow_duplicate=True),
#           Output('freq-sliding','figure',allow_duplicate=True),

#           Input('ranges-sliding','data'),
#           Input('delta-V-sliding', 'value'),
          
#           State('shared-data', 'data'),
#           State('x_cte_data-sliding','data'),
#           State('curr-stepsize-bcte','data'),
#           prevent_initial_call=True
# )
# def update_fourier_data(ranges,dv,data,x_cte_data,curr_stepSize):
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
    
#     const_val_sel = ranges['V_rang'][1] #ranges['B_rang'][1] #esto es x intuicion
#     window_size_val = utpj.tryfloat(dv)
#     B_rang = ranges['B_rang']
#     V_rang = ranges['V_rang']
    
#     const_val_idx,window_size_idxs = suut.get_idx_const_ws(x_cte_data['sec'],
#                                                       x_cte_data['x'],
#                                                       const_val_sel,
#                                                       window_size_val)
    
#     xy_di,_ = suut.get_xy_di(B,V,r,const_val_idx,x_cte_data['xname'],
#                         B_rang,V_rang)
    
#     fwd = suut.get_windowed_fourier(xy_di,window_size_idxs,curr_stepSize)
    
#     fig_rec = Patch()
#     fig_freq = Patch()
#     fig_rec.layout.shapes[0].update(x0=xy_di['x'][0],
#                                 x1=xy_di['x'][window_size_idxs])
#     fig_rec.data[0].update(xy_di)
#     freq,signal_f = suut.datadic_elem_to_arrdata(fwd['0'])
#     fig_freq.data[0].update(x=freq,
#                             y=np.abs(signal_f))
#     return fwd,fig_rec,fig_freq
   
   
# @callback(Output('ranges-sliding','data'),
#           Input('Vmin-sliding', 'value'),
#           Input('Vmax-sliding', 'value'),
#           Input('Bsel-sliding', 'value'),
#           State('ranges-sliding','data'),
#           State('shared-data', 'data'),
#           State('x_cte_data-sliding','data'),
#           prevent_initial_call=True)
# def update_ranges(xm,xM,vs,ranges,data,x_cte_data):
    
#     xm = utpj.tryfloat(xm)
#     xM = utpj.tryfloat(xM)
#     vs = utpj.tryfloat(vs)
#     if None in [xm,xM,vs]:
#         return no_update
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
#     x_cte_data = suut.to_np_arrays_in_dic(x_cte_data)
#     idx_xm = np.argmin(np.abs(x_cte_data['x'] - xm ))
#     idx_xM = np.argmin(np.abs(x_cte_data['x'] - xM ))
#     idx_vs = np.argmin(np.abs(x_cte_data['sec'] - vs ))
    
#     #aca el que cambia es V    
#     ranges['V_rang'] = [idx_xM,0,idx_xm] #inverted
#     ranges['B_rang'] = [0,idx_vs,-1]
#     if vs is None:
#         return no_update
#     ranges['const_val_idx'] = idx_vs

#     return ranges




# @callback(Output('interval-dv','interval'),
#           Input('btn-play','n_clicks'),
#           )
# def set_interval(nc):
#     if nc%2: #estoy en play fijo interval to 1000
#         return 200
#     else:
#         return 60*60*24*1000 #un día







# @callback(Output('curr-stepsize-bcte','data'),
#           Output('step-V-sliding','value'), #es en V 
#           Input('step-V-sliding', 'value'),
#           State('x_cte_data-sliding','data'),
#           prevent_initial_call=True)
# def update_step(step,x_cte_data):
#     dx =  abs(x_cte_data['x'][1] - x_cte_data['x'][0])
#     step = utpj.tryfloat(step)
#     step_idx = max(int(step/dx),1)
#     step = dx*step_idx
#     return step_idx,step




# -----------------------------------------------------------------------
# ------------------------------ Callbacks used to Vcte ------------------------------
# -----------------------------------------------------------------------

def find_index(x,xmin):
    idx = np.argmin(np.abs(x-xmin))
    return idx

from dash import MATCH,no_update,ALL,ctx, clientside_callback,ClientsideFunction

#el primer callback debería tomar la información del input group
# y en base a eso guardar la señal correspondiente,
# calcular el tamaño de ventana y las transformadas de fourier. {fourier-data, }
#fourier-data xcte_data? y slicing data (valores de posición tamaño de paso etc)
@callback( Output({'type': MATCH, 'id': 'slicing-data'}, 'data', allow_duplicate=True),
           Output({'type': MATCH, 'id': 'fourier-data'}, 'data', allow_duplicate=True),
           #Output({'type': MATCH, 'id': 'sliding'}, 'figure',    allow_duplicate=True),
           #Output({'type': MATCH, 'id': 'freq'}, 'figure',       allow_duplicate=True),
           Output({'type': MATCH, 'id': 'update-graph'},'data',  allow_duplicate=True),

           
           Input( {'type': MATCH, 'id': 'xmin'},       'value'),
           Input( {'type': MATCH, 'id': 'xmax'},       'value'),
           Input( {'type': MATCH, 'id': 'sel'},        'value'),
           Input( {'type': MATCH, 'id': 'delta-x'},    'value'),
           Input( {'type': MATCH, 'id': 'step-x'},     'value'),
           State( {'type': MATCH, 'id': 'x_cte_data'}, 'data' ),
           State( {'type': MATCH, 'id': 'sliding'},    'figure' ),
           prevent_initial_call=True) 
def update_data_from_inputs(xmin,xmax,sel,delta_x,step_x,x_cte_data,fig):
    print( 'update_data_from_inputs..')
    
    x = np.array(x_cte_data['x'])
    xname = x_cte_data['xname']
    sec = np.array(x_cte_data['sec'])
    secname = x_cte_data['secname']
    idx_max = find_index(x,utpj.tryfloat(xmin)) #end value
    idx_min = find_index(x,utpj.tryfloat(xmax)) #start value
    idx_sel = find_index(sec,utpj.tryfloat(sel))
    idx_ws  = int(utpj.tryfloat(delta_x)/abs(x[1]-x[0])) #window_size
    step_idx = int(utpj.tryfloat(step_x)/abs(x[1]-x[0]))
    step_idx = max(step_idx,1)

    B,V,r = pgut.get_BVr()
    xi_di,selected_ranges = suut.get_xy_di(B,V,r,
                                           idx_sel,xname,
                                           idx_min,
                                           idx_max)
    slicing_data = {'pos_idx':0, #in indices
                    'play':False,
                    'stepsize':step_idx,
                    'n_points': ((idx_max-idx_ws)-idx_min)//step_idx,
                    'window_size_idx':idx_ws,
                    'const_val_idx': idx_sel,
                    'xmin':idx_min,
                    'xmax':idx_max,
                    }
    
    fourier_data = suut.get_windowed_data(xi_di,slicing_data)

    # update figures

    # fig = Patch()
    # fig['data'][0].update(xi_di)
    # fig['layout']['shapes'][0]['x0'] = xi_di['x'][0]
    # fig['layout']['shapes'][0]['x1'] = xi_di['x'][idx_ws]
    # fig_freq = Patch()

    #print('inside cb')
    #print(len(fourier_data),fourier_data.keys())
    #print(slicing_data)
    return slicing_data,fourier_data,1 #, fig,no_update#fig, fig_freq


clientside_callback(
    ClientsideFunction(
        namespace= 'clientside_sliding_window',
        function_name= 'update_graphs'
    ),
    [
    Output({'type': MATCH, 'id': 'sliding'}, 'figure',    allow_duplicate=True),
    Output({'type': MATCH, 'id': 'freq'},    'figure',    allow_duplicate=True),
    ],
    [Input({'type': MATCH, 'id': 'update-graph'},'data'),
     State({'type': MATCH, 'id': 'fourier-data'}, 'data'),
     State({'type': MATCH, 'id': 'slicing-data'}, 'data'),
     State({'type': MATCH, 'id': 'x_cte_data'},   'data'),
     State('shared-data', 'data'),
     State({'type': MATCH, 'id': 'sliding'}, 'figure'),
     State({'type': MATCH, 'id': 'freq'},    'figure'),
    ],
    prevent_initial_call=True
)
        
    
#stop button
clientside_callback(
       ClientsideFunction(
      namespace='clientside_sliding_window',
      function_name= 'stop_button'  
    ),
    [Output({'type':MATCH, 'id': 'btn-play'}, 'n_clicks', allow_duplicate=True),
     Output({'type':MATCH, 'id': 'btn-play'}, 'className',allow_duplicate=True),
     Output({'type':MATCH, 'id': 'slicing-data'}, 'data',allow_duplicate=True),
     Output({'type':MATCH, 'id': 'update-graph'},'data', allow_duplicate=True),
     ],
    
    [Input({'type':MATCH, 'id': 'btn-stop'}, 'n_clicks'),
     State({'type':MATCH, 'id': 'slicing-data'}, 'data'),
     State({'type':MATCH, 'id': 'btn-play'}, 'n_clicks'),],
    prevent_initial_call=True    
)

#play button
clientside_callback(
    ClientsideFunction(
      namespace='clientside_sliding_window',
      function_name= 'play_button'  
    ),
    [Output({'type':MATCH, 'id': 'btn-play'}, 
                'className',  allow_duplicate=True),
     Output({'type':MATCH, 'id': 'slicing-data'}, 
                'data',  allow_duplicate=True),
     Output({'type':MATCH, 'id': 'interval'}, 
                'interval',  allow_duplicate=True),
    ],
    [Input({'type':MATCH, 'id': 'btn-play'},     'n_clicks'),
     State({'type':MATCH, 'id': 'slicing-data'}, 'data'    ),
    ],

    prevent_initial_call=True
)

#tengo un problema cuando termina, estoy checkeando mal alguna condición o algo
#creo qeu si lo paso a archivo aparte es más facil debugear
#tengo otro bug cuando dejo el step por defecto

#on interval update figs
clientside_callback(
       ClientsideFunction(
      namespace='clientside_sliding_window',
      function_name= 'update_figs_play'  
    ),
    [
     Output({'type':MATCH, 'id': 'update-graph'},'data', allow_duplicate=True),
     Output({'type':MATCH, 'id': 'slicing-data'}, 'data', allow_duplicate=True),
     Output({'type':MATCH, 'id': 'btn-stop'}, 'n_clicks', allow_duplicate=True),
     ],
    [Input({'type':MATCH, 'id': 'interval'},     'n_intervals' ),
     State({'type':MATCH, 'id': 'slicing-data'}, 'data'        ),
    ],
    prevent_initial_call=True     
)


clientside_callback(
    ClientsideFunction(
        namespace='clientside_sliding_window',
        function_name='update_position_btns'
        ),
    [
     Output({'type':MATCH, 'id': 'slicing-data'}, 'data', allow_duplicate=True),
     Output({'type':MATCH, 'id': 'update-graph'},'data', allow_duplicate=True),
    ],
    
    [Input({'type':MATCH, 'id': 'btn-faststepback'}, 'n_clicks'),
     Input({'type':MATCH, 'id': 'btn-stepback'},     'n_clicks'),
     Input({'type':MATCH, 'id': 'btn-stepforward'},  'n_clicks'),
     Input({'type':MATCH, 'id': 'btn-faststepforward'}, 'n_clicks'),
     State({'type':MATCH, 'id': 'slicing-data'}, 'data'),
    ],
    prevent_initial_call=True
        
)