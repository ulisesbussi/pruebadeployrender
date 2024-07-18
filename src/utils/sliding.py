import dash
import dash_bootstrap_components as dbc
from utils import pajama as utpj
from utils import page as pgut

import numpy as np


def get_inputs_and_texts(B,V,x_cte_data = None):
    if x_cte_data is None:
        raise ValueError('x_cte_data must be a dict with keys: x,xname,sec,secname')
    x,xname     = x_cte_data['x'],   x_cte_data['xname']
    sec,secname = x_cte_data['sec'], x_cte_data['secname']
            
    inp_min_slid = dbc.Input(id=f"{xname}min-sliding", 
                         value=f"{x.min():.4f}",debounce=True)
    inp_max_slid = dbc.Input(id=f"{xname}max-sliding",
                         value=f"{x.max():.4f}",debounce=True)
    inp_trace_sel = dbc.Input(id=f"{secname}sel-sliding",
                              value=f"{sec.mean():.4f}",debounce=True)
    inp_window_size = dbc.Input(id=f"delta-{xname}-sliding",
                                value=f"{(x.max()-x.min())/6:.4f}",debounce=True)
    inp_step_size = dbc.Input(id=f"step-{xname}-sliding",
                              value=f"{(abs(x[1]-x[0]))/6:.4f}",debounce=True)
    text_min_slid = dbc.InputGroupText(f"{xname}min")
    text_max_slid = dbc.InputGroupText(f"{xname}max")
    text_trace_sel = dbc.InputGroupText(f"{secname}sel")
    text_window_size = dbc.InputGroupText(f"{xname} window size")
    text_step_size = dbc.InputGroupText(f"{xname} step")
    return dbc.InputGroup([text_trace_sel,inp_trace_sel,
                            text_min_slid,inp_min_slid,
                            text_max_slid,inp_max_slid,
                            text_window_size,inp_window_size,
                            text_step_size,inp_step_size,])


def get_idx_const_ws(sec,x,const_val_sel,window_size_val):
    """esta función será parte del algún utils para obtener los índices en el vector"""
    const_val_sel = utpj.tryfloat(const_val_sel)
    sec = np.array(sec)
    #recupero el indice del valor seleccionado para la sección cte
    const_val_idx = np.argmin(np.abs(sec - const_val_sel )) 
    #calculo cuantos índices tiene la ventana
    window_size_idxs = int(abs(window_size_val/ (x[1]-x[0]))) #in indices
    return const_val_idx,window_size_idxs


# #old
# def get_xy_di(B,V,r,const_val_idx,xname,B_rang=None,V_rang=None):
#     """también al utils"""
#     if xname=='V':
#         B_rang = [0,const_val_idx,-1] if B_rang is None else B_rang
#         V_rang = [0,0,-1] if V_rang is None else V_rang
#         xy_di = utpj.update_Bcte_val(B,V,r,B_rang,V_rang,vertical=False)
#     else:
#         B_rang = [0,0,-1] if B_rang is None else B_rang
#         V_rang = [0,const_val_idx,-1] if V_rang is None else V_rang
#         xy_di = utpj.update_Vcte_val(B,V,r,B_rang,V_rang,vertical=False)

#     return xy_di, {'B_rang':B_rang,'V_rang':V_rang}


def get_xy_di(B,V,r,
              const_val_idx,
              xname,
              x_start=0,x_end=-1,
              B_rang=None,V_rang=None):
    """también al utils"""

    if xname=='V':
        B_rang = [0,const_val_idx,-1] if B_rang is None else B_rang
        V_rang = [x_start,0,x_end] if V_rang is None else V_rang
        xy_di = utpj.update_Bcte_val(B,V,r,B_rang,V_rang,vertical=False)
    else:
        B_rang = [x_start,0,x_end] if B_rang is None else B_rang
        V_rang = [0,const_val_idx,-1] if V_rang is None else V_rang
        xy_di = utpj.update_Vcte_val(B,V,r,B_rang,V_rang,vertical=False)

    return xy_di, {'B_rang':B_rang,'V_rang':V_rang}


def get_windowed_data(xy_di,slicing_data):
    #slicing data is a dict with keys: [pos_idx,play,stepsize_idx,
    #n_points,window_size_idxs,const_val_idx]
    #print(slicing_data.keys())
    x = xy_di['x']
    y = xy_di['y']
    n = slicing_data['n_points']
    ws = slicing_data['window_size_idx']
    step = slicing_data['stepsize']
    datadic = {}
    
    for i in range(n):
        ist = i*step
        x_window = x[ist:ist+ws]
        y_window = y[ist:ist+ws]
        freq_f,signal_f = pgut.fourier_transform({'x':x_window,'y':y_window})
        amplitude = np.abs(signal_f)
        phase = np.angle(signal_f)
        try:
            # datadic[str(ist)] = {'freq':freq_f,'signal_real':signal_f.real,
            #                     'signal_imag':signal_f.imag}
            datadic[str(ist)] = {'freq':freq_f,'amplitude':amplitude,
                                'phase':phase}
        except AttributeError as e:
            print(e)
            #datadic[str(i)] = {'freq':[],'signal_real':[],'signal_imag':[]}
            datadic[str(i)] = {'freq':[],'amplitude':[],'phase':[]}
    return datadic

# #old?
def get_windowed_fourier(xy_di,ws,step=1):
    """esta función será parte del algún utils para obtener los índices en el vector"""
    x = xy_di['x']
    y = xy_di['y']
    # para i [0,1,...,n-ws] -> calc fourier
    datadic = {}
    n = int( (len(x)-ws)/step )
    for i in range( n ):
        ist = i*step
        x_window = x[ist:ist+ws]
        y_window = y[ist:ist+ws]
        freq_f,signal_f = pgut.fourier_transform({'x':x_window,'y':y_window})
        try:
            datadic[str(ist)] = {'freq':freq_f,'signal_real':signal_f.real,
                                'signal_imag':signal_f.imag}
        except AttributeError as e:
            print(e)
            datadic[str(i)] = {'freq':[],'signal_real':[],'signal_imag':[]}
    return datadic


def datadic_elem_to_arrdata(datadic_elem):
    freq = np.array(datadic_elem['freq'])
    signal_f = np.array(datadic_elem['signal_real']) +\
                1j*np.array(datadic_elem['signal_imag'])
    return freq,signal_f

def datadic_elem_to_arrdata2(datadic_elem):
    freq = np.array(datadic_elem['freq'])
    amplitude = np.array(datadic_elem['amplitude'])
    phase = np.array(datadic_elem['phase'])
    signal = amplitude*np.exp(1j*phase)
    return freq,signal

def to_np_arrays_in_dic(x_cte_data):
    x_cte_data['x'] = np.array(x_cte_data['x'])
    x_cte_data['sec'] = np.array(x_cte_data['sec'])
    return x_cte_data