from dash import Input, Output, Patch, State, callback, ctx, no_update, dcc

from utils import page as pgut


# ---------------------- Info ----------------------
""" Tengo por spectral solos 2 callbacks.
1) update_selected_ranges: actualiza un estado de rangos seleccionados, para 
inferir en la modificación de los gráficos y del Fourier
2) update_freq_graph_Xcte: actualiza los gráficos de spectral:
    a- grafico de frecuencias: el grafico que tiene la figura de valor abs y fase 
        de  la fft.
        - En este caso, el gráfico cuenta con cuatro trazas, 0 y 2 en (1,1) y
        1 y 3 en (2,1). 0 y 1 son las transformadas, 2 y 3 los puntos seleccionados.
        3 en realidad no se usa pero se agrega para tener ordenados los datos.
        
    b- gráfico que tiene la señal y reconstrucción.
        -Tiene 2 trazas: la señal original y la reconstruccion.
        
Además actualiza los valores límites del slider de componentes.

Disclaimer, acá podría haberse reutilizado el código, generando un template de 
página genérico y ejecutando una u otra función de imágenes y datos en función
de en cuál página se encuentra. Pero dada la limitante de tiempo era más fácil 
Copiar y pegar los objetos cambiando alguna parte del identificador.
Lo mismo con mucho del trabajo hecho en los callbacks podría haberse
modularizado.
"""


#----------------------------------------------------------------
#--------------------------callbacks -vte -----------------------
#----------------------------------------------------------------
#los update_freq_graph merecen un refactor. Funcionan pero podrían ser
#más claros

#callback que actualiza los rangos desde slider
@callback(Output('selected-ranges-vcte','data'),
          Input('rgslider-b-pajama','value'),
          Input('rgslider-v-pajama','value'),
          prevent_initial_call=True,
        )
def update_selected_ranges_vcte(b_ranges,v_ranges):
    sel_ranges = {'Br':b_ranges,'Vr':v_ranges}
    return sel_ranges


@callback(Output('freq-graph-vcte', 'figure'),#figura de frecuencias
          Output('graph-vcte',      'figure'), #figura de la señal y reconstrucción
          
          Output('selected-freqs-vcte',    'data'),#datos almacenados frecuencias seleccionadas
          
          Output('n_comps-vcte', 'max'),# valor máximo slider de componentes
          Output('n_comps-vcte', 'value'),# valor actual slider de componentes
          Output('n_comps-vcte', 'marks'),# marcas del slider de componentes
          
          Input('n_comps-vcte',        'value'),
          Input('selected-ranges-vcte', 'data'),#datos de rangos seleccionados
          Input('freq-graph-vcte',      'clickData'),# datos de click en gráfica de frecuencias
          
          State('shared-data',          'data'),#datos compartidos
          State('selected-freqs-vcte',  'data'),#datos de frecuencias seleccionadas
          prevent_initial_call=True,
        )
def update_freq_graph_vcte(n_comps, selected_ranges, clickData, 
                           data, selected_points):
    event = ctx.triggered_id
    _update_freq_points= False
    fourier_fig_patched     = Patch()
    reconstruct_fig_patched = Patch()
    
    di_bbrr         = pgut.get_v_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(di_bbrr)
    freq_data       = pgut.get_freq_data(freq_f,signal_f)
    n = len(signal_f)
 
    #vamos a analizar los eventos por orden de entrada:
    #si cambia el slider: actualizo la figura con el nuevo numero
    # y borro los puntos de la figura de frecuencias (y los datos)
    if event == 'n_comps-vcte':#slider
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                        signal_f,
                                        size=len(di_bbrr['x']),
                                        n_comps=n_comps)
        reconstruct_fig_patched.data[-1].update({'x':di_bbrr['x'],'y':rsig})
        selected_points = []
        _update_freq_points= True

    #los valores de slider los cambio si cambiaron los rangos
    if event == 'selected-ranges-vcte':#sliders-pajama
        #change slider
        max_slider_val,\
            current_slider_val,\
            slider_marks          = pgut.update_freq_comp_slider(n)
        for k,v in freq_data.items(): #change patched figure
            fourier_fig_patched.data[k].update(**v)
        reconstruct_fig_patched.data[0].update({'x':di_bbrr['x'],
                                                'y':di_bbrr['y']})
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                            signal_f,
                                            size=len(di_bbrr['x']),
                                            n_comps=n_comps)
        reconstruct_fig_patched.data[1].update({'x':di_bbrr['x'],'y':rsig}) 
        _update_freq_points= True
        selected_points = []
    else:
        max_slider_val     = no_update
        current_slider_val = no_update
        slider_marks       = no_update

    
    #si hay click en grafico o actualizo por slider
    if event == 'freq-graph-vcte':
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
                                                selected_points, size = len(di_bbrr['x']))
        reconstruct_fig_patched.data[-1].update({'x':di_bbrr['x'],'y':rsig})      

    return fourier_fig_patched, reconstruct_fig_patched,\
           selected_points, max_slider_val,\
           current_slider_val, slider_marks




#----------------------------------------------------------------
#--------------------------callbacks b-cte-----------------------
#----------------------------------------------------------------

#callback que actualiza los rangos desde slider
@callback(Output('selected-ranges-bcte','data'),
          Input('rgslider-b-pajama','value'),
          Input('rgslider-v-pajama','value'),
          prevent_initial_call=True,
        )
def update_selected_ranges_bcte(b_ranges,v_ranges):
    sel_ranges = {'Br':b_ranges,'Vr':v_ranges}
    return sel_ranges


@callback(Output('freq-graph-bcte', 'figure'),#figura de frecuencias
          Output('graph-bcte',      'figure'), #figura de la señal y reconstrucción
          
          Output('selected-freqs-bcte',    'data'),#datos almacenados frecuencias seleccionadas
          
          Output('n_comps-bcte', 'max'),# valor máximo slider de componentes
          Output('n_comps-bcte', 'value'),# valor actual slider de componentes
          Output('n_comps-bcte', 'marks'),# marcas del slider de componentes
          
          Input('n_comps-bcte',        'value'),
          Input('selected-ranges-bcte', 'data'),#datos de rangos seleccionados
          Input('freq-graph-bcte',      'clickData'),# datos de click en gráfica de frecuencias
          
          State('shared-data',          'data'),#datos compartidos
          State('selected-freqs-bcte',  'data'),#datos de frecuencias seleccionadas
          prevent_initial_call=True,
        )
def update_freq_graph_bcte(n_comps, selected_ranges, clickData, 
                           data, selected_points):
    event = ctx.triggered_id
    _update_freq_points= False
    fourier_fig_patched     = Patch()
    reconstruct_fig_patched = Patch()
    
    di_vvrr         = pgut.get_b_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(di_vvrr)
    freq_data       = pgut.get_freq_data(freq_f,signal_f)
    n = len(signal_f)
 
    #vamos a analizar los eventos por orden de entrada:
    #si cambia el slider: actualizo la figura con el nuevo numero
    # y borro los puntos de la figura de frecuencias (y los datos)
    if event == 'n_comps-bcte':#slider
        rsig,_,pfreqs = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                    signal_f,
                                    size=len(di_vvrr['x']),
                                    n_comps=n_comps)
        reconstruct_fig_patched.data[-1].update({'x':di_vvrr['x'],'y':rsig})
        selected_points = []
        _update_freq_points= True

    #los valores de slider los cambio si cambiaron los rangos
    if event == 'selected-ranges-bcte':#sliders-pajama
        #change slider
        max_slider_val,\
            current_slider_val,\
            slider_marks          = pgut.update_freq_comp_slider(n)
        for k,v in freq_data.items(): #change patched figure
            fourier_fig_patched.data[k].update(**v)
        reconstruct_fig_patched.data[0].update({'x':di_vvrr['x'],
                                                'y':di_vvrr['y']})
        rsig,_,_ = pgut.reconstruct_w_n_comps(freq_f, #new reconstruct signal
                                            signal_f,
                                            size=len(di_vvrr['x']),
                                            n_comps=n_comps)
        reconstruct_fig_patched.data[1].update({'x':di_vvrr['x'],'y':rsig})
        _update_freq_points= True
        selected_points = []
    else:
        max_slider_val     = no_update
        current_slider_val = no_update
        slider_marks       = no_update

    
    #si hay click en grafico o actualizo por slider
    if event == 'freq-graph-bcte':
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
                                                selected_points, size = len(di_vvrr['x']))
        reconstruct_fig_patched.data[-1].update({'x':di_vvrr['x'],'y':rsig})      
    
    return fourier_fig_patched, reconstruct_fig_patched,\
           selected_points, max_slider_val,\
           current_slider_val, slider_marks



@callback(Output('download-vcte','data'),
          
          Input('btn-fourier-vcte','n_clicks'),
          Input('btn-rec-vcte','n_clicks'),
          
          State('n_comps-vcte', 'value'),
          State('selected-ranges-vcte', 'data'),#datos de rangos seleccionados          
          State('shared-data',          'data'),#datos compartidos
          State('selected-freqs-vcte',  'data'),#datos de frecuencias seleccionadas

        prevent_initial_call=True,
        )          
def download_freq_vcte(btn1, btn2, n_comps, selected_ranges,
                       data, selected_points):
    event = ctx.triggered_id
    
    data_di = pgut.get_v_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(data_di)

    if event == 'btn-fourier-vcte':
        csv,name = pgut.download_fourier(freq_f,signal_f,
                                     data,selected_ranges,vcte=True)
        return dcc.send_data_frame(csv,name)
    
    if event == 'btn-rec-vcte':
        
        bb,rr = data_di['x'], data_di['y']
        if len(selected_points):
            rsig,comp_freqs,_ = pgut.reconstruct_w_selected(freq_f,
                                                    signal_f,
                                                    selected_points,
                                                    size = len(bb))
            di = pgut.get_v_trace(data,selected_ranges)
            sel_freqs = freq_f[selected_points]
        else: #reconstruction with n_comps
            rsig,comp_freqs,p_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                    signal_f,
                                                    size = len(bb),
                                                    n_comps=n_comps)
            di = pgut.get_v_trace(data,selected_ranges)
            sel_freqs = freq_f[p_freqs]

        csv,name = pgut.download_reconstruction(bb,rsig,comp_freqs,sel_freqs)
        return dcc.send_data_frame(csv,name)




@callback(Output('download-bcte','data'),
          
          Input('btn-fourier-bcte','n_clicks'),
          Input('btn-rec-bcte','n_clicks'),
          
          State('n_comps-bcte', 'value'),
          State('selected-ranges-bcte', 'data'),#datos de rangos seleccionados          
          State('shared-data',          'data'),#datos compartidos
          State('selected-freqs-bcte',  'data'),#datos de frecuencias seleccionadas

        prevent_initial_call=True,
        )          
def download_freq_bcte(btn1, btn2, n_comps, selected_ranges,
                       data, selected_points):
    event = ctx.triggered_id
    
    data_di = pgut.get_b_trace(data,selected_ranges)
    freq_f,signal_f = pgut.fourier_transform(data_di)

    if event == 'btn-fourier-bcte':
        csv,name = pgut.download_fourier(freq_f,signal_f,
                                     data,selected_ranges,vcte=False)
        return dcc.send_data_frame(csv,name)
    
    if event == 'btn-rec-bcte':
        
        vv,rr = data_di['x'], data_di['y']
        if len(selected_points):
            rsig,comp_freqs,_ = pgut.reconstruct_w_selected(freq_f,
                                                    signal_f,
                                                    selected_points,
                                                    size = len(vv))
            di = pgut.get_v_trace(data,selected_ranges)
            sel_freqs = freq_f[selected_points]
        else: #reconstruction with n_comps
            rsig,comp_freqs,p_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                    signal_f,
                                                    size = len(vv),
                                                    n_comps=n_comps)
            di = pgut.get_v_trace(data,selected_ranges)
            sel_freqs = freq_f[p_freqs]

        csv,name = pgut.download_reconstruction(vv,rsig,comp_freqs,sel_freqs)
        return dcc.send_data_frame(csv,name)
