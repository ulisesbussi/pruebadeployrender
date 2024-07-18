
from dash import (Input, Output, State, no_update,
            callback,callback_context, Patch, ctx, dcc)
import pandas as pd
import base64
from io import StringIO
import numpy as np

from utils import pajama as utpj
from utils import page as pgut


@callback(Output('data-uploaded',      'data', allow_duplicate=True),
          Output('proc-data-uploaded', 'data', allow_duplicate=True),
          
          Input('upload-data',            'contents'),
          Input('toggle-switch-uploaded', 'value'),
          prevent_initial_call=True)

def load_data(contents, toggle_val):
    event = ctx.triggered_id
    
    #contents is plain text base64 encoded convert to read with pandas
    contents = contents.split(",")[1]
    contents = base64.b64decode(contents).decode("utf-8")

    data = pd.read_csv(StringIO(contents),sep='\t',names=['B','V','r'])

    di= {'B':data['B'].tolist(),'V':data['V'].tolist(),'r':data['r'].tolist()}
    #parsing data, separating by V vals
    di_proc={}
    di_proc['uniques'] = {'B':np.unique(data['B']).tolist(),
                          'V':np.unique(data['V']).tolist()}
    
    di_proc['sections'] = {}
    
    for vv in di_proc['uniques']['V']:
        this_raw_B = data[data['V']==vv]['B']
        this_raw_r = data[data['V']==vv]['r']
        idx_max = np.argmax(this_raw_B)
        if toggle_val ==[]: #increasing B (from 0 to idx_max)
            B_crop = this_raw_B.iloc[:idx_max]
            r_crop = this_raw_r.iloc[:idx_max]
        else: #decreasing B (from idx_max to end) and reverse to have B increasing
            B_crop = this_raw_B.iloc[idx_max:][::-1]
            r_crop = this_raw_r.iloc[idx_max:][::-1]
        di_proc['sections'][str(vv)] = {'B':B_crop.tolist(),
                                        'r':r_crop.tolist()}

    return di,di_proc

@callback(Output('V-uploaded',     'value', allow_duplicate=True),
          Output('V-uploaded',     'min',   allow_duplicate=True),
          Output('V-uploaded',     'max',   allow_duplicate=True),
          Output('V-uploaded',     'marks', allow_duplicate=True),
          Output('V_sel-uploaded', 'value', allow_duplicate=True),
          
          Input('data-uploaded',      'data'),
          State('proc-data-uploaded', 'data'),
          prevent_initial_call=True)
def update_selector_v(data, di_proc):

    if not len(data):
        return no_update,no_update,no_update,\
               no_update,no_update

    uniques = di_proc['uniques']['V']
    n = len(uniques)
    
    value= n//2
    imin = 0
    imax = n-1
    if len(uniques) < 15:
        marks = {idx: f'{i}' for idx,i in enumerate(uniques)}
    else:
        marks = {idx: f'{uniques[idx]}' for idx in range(0,n,n//6)}

    vs_val = uniques[value]
    return value,imin,imax,marks,vs_val

@callback(Output('V-uploaded',     'value', allow_duplicate=True),
          Output('V_sel-uploaded', 'value', allow_duplicate=True),
          
          Input('V-uploaded',     'value'),
          Input('V_sel-uploaded', 'value'),
          
          State('data-uploaded',      'data'),
          State('proc-data-uploaded', 'data'),
          prevent_initial_call=True)
def bind_v_inputs(value,vs_val,data, di_proc):
    event = ctx.triggered_id

    if event == 'V-uploaded': #trigger[0]['prop_id'] == 'V-uploaded.value':
        vs_val = str(di_proc['uniques']['V'][value])
        return value,vs_val
    if event == 'V_sel-uploaded':
        value = np.argmin(np.abs(np.array(di_proc['uniques']['V'])-\
                    utpj.tryfloat(vs_val)))
        return value,vs_val
    

@callback(Output('B-uploaded',         'value', allow_duplicate=True),
          Output('B-uploaded',         'min',   allow_duplicate=True),
          Output('B-uploaded',         'max',   allow_duplicate=True),
          Output('B-uploaded',         'marks', allow_duplicate=True),
          Output('proc-data-uploaded', 'data',  allow_duplicate=True),

          Input('V-uploaded', 'value'),
          
          State('data-uploaded',      'data'),
          State('proc-data-uploaded', 'data'),
            prevent_initial_call=True)
def update_selector_B(val,data,di_proc):

    if not len(data):
        return no_update,no_update,no_update,\
               no_update,no_update
    
    #aca tengo que pasar val por uiniques
    vv = di_proc['uniques']['V'][val]
    this_sec = di_proc['sections'][str(vv)]['B']

    n = len(this_sec)
    di_proc['curr_data']= {'B':this_sec,'V':vv,
                        'r':di_proc['sections'][str(vv)]['r']}
    min = 0
    max = n-1
    value= [min,max]
    marks = {idx: f'{this_sec[idx]}' for idx in range(0,n,n//6)}
    
    return value,min,max,marks,di_proc

@callback(Output('B-uploaded',     'value', allow_duplicate=True),
          Output('B_min-uploaded', 'value', allow_duplicate=True),
          Output('B_max-uploaded', 'value', allow_duplicate=True),

          Input('B-uploaded',     'value'),
          Input('B_min-uploaded', 'value'),
          Input('B_max-uploaded', 'value'),

          State('data-uploaded',      'data'),
          State('proc-data-uploaded', 'data'),
          prevent_initial_call=True)
def bind_b_inputs(val,bm_val,bM_val,data,di_proc):
    event = ctx.triggered_id
    
    curr_b_val  = np.array(di_proc['curr_data']['B'])
    if event == 'B-uploaded': #trigger[0]['prop_id'] == 'B-uploaded.value':
        bm_val = str(curr_b_val[val[0]])
        bM_val = str(curr_b_val[val[1]])
    if event == 'B_min-uploaded': #trigger[0]['prop_id'] == 'B_min-uploaded.value':
        val = np.argmin(curr_b_val-utpj.tryfloat(bm_val))
    if event == 'B_max-uploaded':#trigger[0]['prop_id'] == 'B_max-uploaded.value':
        val = np.argmin(curr_b_val-utpj.tryfloat(bM_val))

    return val,bm_val,bM_val
        


@callback(Output('freq-graph-uploaded', 'figure',allow_duplicate=True),#figura de frecuencias
          Output('graph-uploaded',      'figure',allow_duplicate=True), #figura de la señal y reconstrucción
          
          Output('selected-freqs-uploaded', 'data'),#datos almacenados frecuencias seleccionadas
          
          Output('n_comps-uploaded', 'max'),# valor máximo slider de componentes
          Output('n_comps-uploaded', 'value'),# valor actual slider de componentes
          Output('n_comps-uploaded', 'marks'),# marcas del slider de componentes
          
          Input('n_comps-uploaded', 'value'), #n comps
          Input('B-uploaded', 'value'), #rango de B
          Input('V-uploaded', 'value'), #valor de v
          Input('freq-graph-uploaded', 'clickData'),# datos de click en gráfica de frecuencias
          
          State('proc-data-uploaded',      'data'),#datos compartidos
          State('selected-freqs-uploaded', 'data'),#datos de frecuencias seleccionadas
          prevent_initial_call=True,
        )
def update_freq_graph_vcte(n_comps, B_val,V_val, clickData, 
                           di_proc, selected_points):
    event = ctx.triggered_id
    _update_freq_points= False
    fourier_fig_patched     = Patch()
    reconstruct_fig_patched = Patch()
    
    curr_data = di_proc.get('curr_data')
    if curr_data is None:
        return no_update,no_update,no_update,\
               no_update,no_update,no_update
    x = np.array(curr_data['B'])[B_val[0]:B_val[1]]
    y = np.array(curr_data['r'])[B_val[0]:B_val[1]]

    freq_f,signal_f = pgut.fourier_transform({'x':x,'y':y})
    freq_f = freq_f[::-1]
    freq_data       = pgut.get_freq_data(freq_f,signal_f)
    n = len(signal_f)
 
    #vamos a analizar los eventos por orden de entrada:
    #si cambia el slider: actualizo la figura con el nuevo numero
    # y borro los puntos de la figura de frecuencias (y los datos)
    if event == 'n_comps-uploaded':#slider
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                        signal_f,
                                        size=len(x),
                                        n_comps=n_comps)
        reconstruct_fig_patched.data[-1].update({'x':x,'y':rsig})
        selected_points = []
        _update_freq_points= True

    #los valores de slider los cambio si cambiaron los rangos
    if event == 'B-uploaded':#sliders-pajama
        #change slider
        max_slider_val,\
            current_slider_val,\
            slider_marks          = pgut.update_freq_comp_slider(n)
        for k,v in freq_data.items(): #change patched figure
            fourier_fig_patched.data[k].update(**v)
        reconstruct_fig_patched.data[0].update({'x':x,
                                                'y':y})
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                            signal_f,
                                            size=len(x),
                                            n_comps=n_comps)
        reconstruct_fig_patched.data[1].update({'x':x, 'y':rsig}) 
        _update_freq_points= True
        selected_points = []
    else:
        max_slider_val     = no_update
        current_slider_val = no_update
        slider_marks       = no_update

    
    #si hay click en grafico o actualizo por slider
    if event == 'freq-graph-uploaded':
        fourier_fig_patched,selected_points = pgut.update_freq_fig_selected(clickData,
                                    selected_points,freq_f,signal_f,
                                    fourier_fig_patched)
    if _update_freq_points:
        fourier_fig_patched.data[2].update({'x':[],'y':[]})
        selected_points = []
    
    #datos seleccionados
    if len(selected_points):
        rsig,_,_ = pgut.reconstruct_w_selected(freq_f,
                                                signal_f,
                                                selected_points, size = len(x))
        reconstruct_fig_patched.data[-1].update({'x':x,'y':rsig})      

    return fourier_fig_patched, reconstruct_fig_patched,\
           selected_points, max_slider_val,\
           current_slider_val, slider_marks


@callback(Output('collapse-uploaded', 'is_open'),
            Input('upload-data', 'contents'),
            prevent_initial_call=True)
def toggle_collapse(contents):
    return True


@callback(Output('download-uploaded', 'data'),
          
          Input('btn-fourier-uploaded', 'n_clicks'),
          Input('btn-rec-uploaded', 'n_clicks'),
          
          State('selected-freqs-uploaded', 'data'),
          State('proc-data-uploaded', 'data'),
          State('n_comps-uploaded', 'value'),
          State('data-uploaded', 'data'),
          State('B-uploaded', 'value'),
          
            prevent_initial_call=True)  
def downloads(btn_f,btn_r,selected_points,di_proc,
              n_comps,data,B_val,):
    event = ctx.triggered_id
    curr_data = di_proc.get('curr_data')

    x = np.array(curr_data['B'])[B_val[0]:B_val[1]]
    y = np.array(curr_data['r'])[B_val[0]:B_val[1]]
    freq_f,signal_f = pgut.fourier_transform({'x':x,'y':y})
    if event == 'btn-fourier-uploaded':
        
        csv = pd.DataFrame({'freq':freq_f,'signal_real':signal_f.real,
                       'signal_imag':signal_f.imag}).to_csv
        #print(csv()[:50])
        name = f"fourier_{curr_data['V']:.3f}_B_from_{B_val[0]:.3f}"+\
               f"_to_{B_val[1]:.3f}.csv"
        return dcc.send_data_frame(csv, name)
    
    if event == 'btn-rec-uploaded':
        if len(selected_points):
            rsig,comp_freqs,p_freqs = pgut.reconstruct_w_selected(freq_f,
                                                signal_f,
                                                selected_points, 
                                                size = len(x))
            sel_freqs = freq_f[selected_points]
        else:
            rsig,comp_freqs,p_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                signal_f,
                                                size = len(x),
                                                n_comps=n_comps)
            sel_freqs = freq_f[p_freqs]    
        
        csv,name = pgut.download_reconstruction(x,rsig,
                                               comp_freqs,
                                                sel_freqs)
        return dcc.send_data_frame(csv, name)