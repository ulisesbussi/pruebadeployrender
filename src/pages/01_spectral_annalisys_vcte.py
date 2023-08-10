import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import (ALL, Dash, Input, Output, Patch, State, callback, ctx, dcc,
                  html, no_update, register_page)
from dash_bootstrap_templates import load_figure_template
from plotly import graph_objs as go

load_figure_template("cyborg")
#from db_manipulation import utils as dbu

import page_utils as pgut
from pages.shared_pajama import shared_pajama

#--------------------------------register-----------------------------
register_page(__name__, path="/vcte-fourier",name = "V-section Fourier")
#---------------------------------------------------------------------



B,V,r = pgut.get_dataset()
data = {'B':B.tolist(),'V':V.tolist(),'r':r.tolist()}

fig,di_bbrr = pgut.trace_v_2d(data)
freq_f,signal_f = pgut.fourier_transform(di_bbrr)
fig_freq = pgut.freq_graph(freq_f,signal_f)

rsig,signals,principal_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                          signal_f,n_comps=10)
fig_rec = pgut.draw_reconstruction(di_bbrr['x'],rsig,fig)


data_freq = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}
data_selected_ranges = {'Br':[0,0,-1],'Vr':[0,0,-1]}

max_n = len(di_bbrr['x'])


#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------

layout = dbc.Container([
    dbc.Row([
       shared_pajama,
      
       dbc.Col([
            dcc.Store(id= 'selected-ranges-vcte', data = data_selected_ranges),
            dcc.Store(id= 'fourier-vals-vcte',    data = data_freq),
            dcc.Store(id= 'di_bbrr-vcte',         data = di_bbrr),
            dcc.Store(id= 'selected-freqs',       data = []),
            html.H1(" Fourier Transform V constant secction",className='title', id='title'),
            dcc.Graph(id='freq-graph-vcte',
                figure= fig_freq),
            dcc.Slider(id='n_comps-vcte',
                min=1,
                max=max_n,
                value= 10,
                step = 1,
                marks={i: f'{i}' for i in range(0,max_n,max_n//6)}),
            dcc.Graph(id='graph-vcte',
                figure=fig,
                ),
       ],className='col50width'),
    ]),
],className="container-flex")
        


#----------------------------------------------------------------
#--------------------------callbacks-----------------------------
#----------------------------------------------------------------

#callback que actualiza los rangos desde slider
@callback(Output('selected-ranges-vcte','data'),
          Input('rgslider-b-pajama-3dplot','value'),
          Input('rgslider-v-pajama-3dplot','value'),
          prevent_initial_call=True,
        )
def update_selected_ranges(b_ranges,v_ranges):
    sel_ranges = {'Br':b_ranges,'Vr':v_ranges}
    return sel_ranges

#callback que actualiza freq-graph
#aca no me tengo que asustar por el rango de la transformada
#el máximo freq viene dado por el dt de la señal
@callback(Output('freq-graph-vcte','figure'),
          Output('fourier-vals-vcte','data'),
          Output('di_bbrr-vcte','data'),
          Output('n_comps-vcte','max'),
          Output('n_comps-vcte','value'),
          Output('n_comps-vcte','marks'),
          Output('selected-freqs','data'),
          Input('selected-ranges-vcte','data'),
          Input('freq-graph-vcte','clickData'),
          State('shared-data','data'),
          State('selected-freqs','data'),
          prevent_initial_call=True,
        )
def update_freq_graph_vcte(selected_ranges,clickData,data,selected_points):
    
    fourier_fig_patched = Patch()
    
    di_bbrr = pgut.get_v_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(di_bbrr)
    freq_data = pgut.get_freq_data(freq_f,signal_f)
    
    #change slider
    n = len(signal_f)
    max_slider_val,\
        current_slider_val,\
        slider_marks          = pgut.update_freq_comp_slider(n)

    for k,v in freq_data.items(): #change patched figure
        fourier_fig_patched.data[k].update(**v)
    fourier_di = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}

    if ctx.triggered[0]['prop_id'] == 'freq-graph-vcte.clickData':
        #print(clickData)
        fourier_fig_patched,selected_points = update_freq_fig_selected(clickData,
                                    selected_points,freq_f,signal_f,
                                    fourier_fig_patched)
       #fourier_fig_patched.data[3].update(line_color='red')

    return fourier_fig_patched, fourier_di, di_bbrr,\
            max_slider_val,current_slider_val,slider_marks,selected_points



def update_freq_fig_selected(clickData,selected_points,
                             freq_f,signal_f,freq_fig_patched):
    #print(selected_points)
    curveNumber = clickData['points'][0]['curveNumber']
    if curveNumber not in [0,2]:
        return no_update,selected_points
    print(clickData)
    idx = clickData['points'][0]['pointIndex']
    if curveNumber == 0:
        if idx in selected_points:
            selected_points.remove(idx)
        else:
            selected_points.append(idx)
    else:
        selected_points.pop(idx)
    print(selected_points)
    di= {'x': freq_f[selected_points],'y':np.abs(signal_f[selected_points])}
    print(di)
    freq_fig_patched.data[2].update(di)
    return freq_fig_patched,selected_points


#TODO: tengo que hacer que el slider resetee los selected points, incluso podría
#hacer que me los sobreescriba y mostrar cuales son las que el slider está seleccionando...
#creo que me conviene pasar los callbacks a scripts aparte, y las funciones
#que se encargan de los mismos podrían ser genéricas para las 2 paginas?

#callback que actualiza el gráfico de señal y reconstrucción
@callback(Output('graph-vcte','figure'),
          Input('n_comps-vcte','value'),
          Input('fourier-vals-vcte','data'),
          Input('selected-freqs','data'),
          State('di_bbrr-vcte','data'),
          prevent_initial_call=True,
          )
def change_n_comps(n_comps,data,selected_points, di_bbrr):
    freq_f = data.get('freq')
    signal_f_r = data.get('signal_real') 
    signal_f_i = data.get('signal_imag')
    if freq_f is None:
        return no_update
    signal_f = np.array(signal_f_r) + 1j*np.array(signal_f_i)

    if len(selected_points):
        rsig,_,_ = pgut.reconstruct_w_selected(freq_f,signal_f,selected_points)
    else:
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f,
                                            signal_f,n_comps=n_comps)

    patched_fig = Patch()
    
    bb = di_bbrr['x']
    rr = di_bbrr['y']
    
    patched_fig.data[0].update({'x':bb,'y':rr})
    patched_fig.data[-1].update({'x':bb,'y':rsig})

    return patched_fig

# Es por acá, no es trivial, pero debería checkear
# Debería agregar un trace vacio sobre el primer subplot, de este modo
# puedo agregar o quitar puntos ahí.
# luego debería también mirar los puntos que hay para la transformada de fourier?
#"ufff"
# @callback(Output('freq-graph-vcte','figure'),
#           Input('freq-graph-vcte','clickData'),
#         )
# def update_click_data(clickData):
#     print(clickData)
#     if clickData is None:
#         return 'Fourier Transform V constant secction'
#     else:
#         return f'{clickData}'