import dash_bootstrap_components as dbc
from dash import dcc, html, register_page
from dash_bootstrap_components import Col, Row
import numpy as np

from dash_bootstrap_templates import load_figure_template
load_figure_template("slate")

from utils import page as pgut
from utils import pajama as utpj
from utils import sliding as suut
from pages.shared_pajama import shared_pajama

#--------------------------------register-----------------------------
register_page(__name__, path="/sliding-fourier-Bcte",
              name = "Sliding Fourier constant B")
#---------------------------------------------------------------------



B,V,r = pgut.dd
data = pgut.dd_data
#x_cte_data es el vector que dice quien es x y quien el valor cte
x_cte_data = {'x':V,'xname':'V','sec':B,'secname':'B','r':r}

typedic = {'type':'bcte-fourier-sliding'} #type associate to page vcte fourier
#----------------------------------------------------------------
#-------- buttons Col -----------------------------------------


def create_control_btns_col(typedic):
    
    id_symbols = [ ('btn-faststepback','fa-fast-backward'),
                   ('btn-stepback','fa-backward'),
                   ('btn-play','fa-play'),
                   ('btn-stop','fa-stop'),
                   ('btn-stepforward','fa-forward'),
                   ('btn-faststepforward','fa-fast-forward')]
    btns = []
    for id,sym in id_symbols:    
        btns.append(dbc.Button("", id={**typedic,'id':id},
                                n_clicks=0, className=f"fa {sym} mr1"))
    return Col(btns,width=4)


def get_inputs_and_texts(typedic,x_cte_data = None):

    x,xname     = x_cte_data['x'],   x_cte_data['xname']
    sec,secname = x_cte_data['sec'], x_cte_data['secname']

    text_id_vals = [ 
            (f'{secname}sel', 'sel', f'{sec.mean():.4f}'),
            (f'{xname}min', 'xmin', f'{x.min():.4f}'),
            (f'{xname}max', 'xmax', f'{x.max():.4f}'),           
            (f'{xname} window size', 'delta-x', f'{(x.max()-x.min())/6:.4f}'),
            (f'{xname} step', 'step-x', f'{(abs(x[1]-x[0]))/6:.4f}'),
            ]
    
    inputs = dbc.InputGroup([])
    for text,id,val in text_id_vals:
        inputs.children.append(dbc.InputGroupText(text))
        inputs.children.append(dbc.Input(id={**typedic,'id':id},
                                            value=val,debounce=True))
    return inputs



inputs = Col([get_inputs_and_texts(typedic,x_cte_data),])

control_buttons = create_control_btns_col(typedic)



const_val_sel   = x_cte_data['sec'].mean()
window_size_val = (x_cte_data['x'].max()-x_cte_data['x'].min())/6


const_val_idx,window_size_idxs =suut.get_idx_const_ws(x_cte_data['sec'],
                                                  x_cte_data['x'],
                                                  const_val_sel,
                                                  window_size_val)

xy_di, _ = suut.get_xy_di(B,V,r,const_val_idx,x_cte_data['xname'],)


fig = utpj.create_fig_and_cnf()
fig = utpj.draw_Vcte_trace(fig, B,V,r) #ACA CAMBIA LA FUNCIÓN
fig.data[0].update(xy_di)
fig.add_vrect(x0=x_cte_data['x'][0], 
              x1=x_cte_data['x'][window_size_idxs], 
              line_width=0, 
              fillcolor="red", 
              opacity=0.2)
fig.update_layout(
    xaxis_title=" V [T]",
    yaxis_title=r"&#916;G <sup> e<sup>2</sup></sup>/<sub>h</sub>")


slicing_data = {'pos_idx':0,
                'play':False,
                'stepsize':1,
                'n_points':len(x_cte_data['x'])-window_size_idxs-1,#unused?
                'window_size_idx':window_size_idxs,
                'const_val_idx':const_val_idx,
                'xmin': 0,
                'xmax': len(x_cte_data['x'])-1}


fwd = suut.get_windowed_data(xy_di, slicing_data)

#TODO: cambiar freq_graph para que tome amplitud y fase
fig_freq = pgut.freq_graph2(*suut.datadic_elem_to_arrdata2(fwd['0']))

fig_freq.update_xaxes(title_text="Freq [Hz]", row=2, col=1)
fig_freq.update_yaxes(title_text="Amplitude", row=1, col=1)
fig_freq.update_yaxes(title_text="Phase [rad]", row=2, col=1)

#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------
#npoints initial value as placeholder

#print(slicing_data)
#print(len(fwd),fwd.keys())
#print(fwd['0'])
layout = dbc.Container([
    Row([
        dcc.Store(id={**typedic, 'id':'x_cte_data'}, 
                  data= x_cte_data),
        dcc.Store(id={**typedic, 'id':'slicing-data'},
                  data=slicing_data),

        
        dcc.Store(id={**typedic,'id':'fourier-data'},
                  data=fwd),
        dcc.Store(id={**typedic,'id':'update-graph'},
                  data=0),
        
        dcc.Interval(id={**typedic,'id':'interval'},
                     interval=60*60*24*1000,n_intervals=0),
        Col([ inputs, 
             control_buttons,
             
             dcc.Graph(id={**typedic,'id':'sliding'}, 
                       figure=fig),
             dcc.Graph(id={**typedic,'id':'freq'},
                      figure=fig_freq),
            ],width=12),

    ]),
],className='h-100 mw-100 container-flex')

