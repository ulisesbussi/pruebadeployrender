from dash import (
                Dash, dcc, html, Input, 
                Output, State ,callback, ALL,
                register_page, Patch,
                ctx, no_update
    )
import dash_bootstrap_components as dbc
import pandas as pd
from plotly import graph_objs as go
from dash_bootstrap_templates import load_figure_template
import numpy as np
load_figure_template("cyborg")


#from db_manipulation import utils as dbu

from pages.shared_pajama import shared_pajama
import page_utils as pgut


#--------------------------------register-----------------------------
register_page(__name__, path="/bcte-fourier",name = "B-section Fourier")
#---------------------------------------------------------------------



B,V,r = pgut.get_dataset()
data = {'B':B.tolist(),'V':V.tolist(),'r':r.tolist()}

fig,di_vvrr = pgut.trace_b_2d(data)
freq_f,signal_f = pgut.fourier_transform(di_vvrr)
fig_freq = pgut.freq_graph(freq_f,signal_f)

rsig,signals,principal_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                          signal_f,n_comps=10)
fig_rec = pgut.draw_reconstruction(di_vvrr['x'],rsig,fig)


data_freq = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}
data_selected_ranges = {'Br':[0,0,-1],'Vr':[0,0,-1]}

max_n = len(di_vvrr['x'])


#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------

layout = dbc.Container([
    dbc.Row([
       shared_pajama,
      
       dbc.Col([
            dcc.Store(id= 'selected-ranges-bcte', data = data_selected_ranges),
            dcc.Store(id= 'fourier-vals-bcte',    data = data_freq),
            dcc.Store(id= 'di_vvrr-bcte',                  data = di_vvrr),

            html.H1(" Fourier Transform B constant secction",className='title'),
            dcc.Graph(id='freq-graph-bcte',
                figure= fig_freq),
            dcc.Slider(id='n_comps-bcte',
                min=1,
                max=max_n,
                value= 10,
                step = 1,
                marks={i: f'{i}' for i in range(0,max_n,max_n//6)}),
            dcc.Graph(id='graph-bcte',
                figure=fig,
                ),
       ],className='col50width'),
    ]),
],className="container-flex")
        


#----------------------------------------------------------------
#--------------------------callbacks-----------------------------
#----------------------------------------------------------------

#callback que actualiza los rangos desde slider
@callback(Output('selected-ranges-bcte','data'),
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
@callback(Output('freq-graph-bcte','figure'),
          Output('fourier-vals-bcte','data'),
          Output('di_vvrr-bcte','data'),
          Output('n_comps-bcte','max'),
          Output('n_comps-bcte','value'),
          Output('n_comps-bcte','marks'),
          Input('selected-ranges-bcte','data'),
          State('shared-data','data'), #this is general
          prevent_initial_call=True,
        )
def update_freq_graph_vcte(selected_ranges,data):
    
    fourier_fig_patched = Patch()
    
    di_vvrr = pgut.get_b_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(di_vvrr)
    freq_data = pgut.get_freq_data(freq_f, signal_f)
    
    #change slider
    n = len(signal_f)
    max_slider_val,\
        current_slider_val,\
            slider_marks      = pgut.update_freq_comp_slider(n)
    
    for k,v in freq_data.items(): #change patched figure
        fourier_fig_patched.data[k].update(**v)
    fourier_di = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}

    return fourier_fig_patched, fourier_di, di_vvrr,\
            max_slider_val,current_slider_val,slider_marks 

#callback que actualiza el gráfico de señal y reconstrucción
@callback(Output('graph-bcte','figure'),
          Input('n_comps-bcte','value'),
          Input('fourier-vals-bcte','data'),
          State('di_vvrr-bcte','data'),
          prevent_initial_call=True,
          )
def change_n_comps(n_comps,data, di_bbrr):
    freq_f = data.get('freq')
    signal_f_r = data.get('signal_real') 
    signal_f_i = data.get('signal_imag')
    if freq_f is None:
        return no_update
    signal_f = np.array(signal_f_r) + 1j*np.array(signal_f_i)

    rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f,
                                        signal_f,n_comps=n_comps)
    patched_fig = Patch()
    
    bb = di_bbrr['x']
    rr = di_bbrr['y']
    
    patched_fig.data[0].update({'x':bb,'y':rr})
    patched_fig.data[-1].update({'x':bb,'y':rsig})
    
    return patched_fig


