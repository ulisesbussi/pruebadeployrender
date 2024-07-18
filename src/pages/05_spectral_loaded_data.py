import dash_bootstrap_components as dbc
from dash import dcc, html, register_page
from dash_bootstrap_components import Col, Row

from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")


from utils import page as pgut
from pages.shared_pajama import shared_pajama

#--------------------------------register-----------------------------
register_page(__name__, path="/load_fourier",name = "Load Fourier")
#---------------------------------------------------------------------

import numpy as np

#initialize void data
B = np.array([])
V = np.array([])
r = np.array([[]])
data = {'B':B.tolist(),'V':V.tolist(),'r':r.tolist()}



fig,di_bbrr = pgut.trace_v_2d(data)
freq_f,signal_f = pgut.fourier_transform(di_bbrr)

fig_freq = pgut.freq_graph(freq_f,signal_f)

rsig,signals,principal_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                          signal_f,size=None,n_comps=10)
fig_rec = pgut.draw_reconstruction(di_bbrr['x'],rsig,fig)

data_freq = {'freq':freq_f,'signal_real':[-1,],
                            'signal_imag':[-1]}

# data_freq = {'freq':freq_f,'signal_real':signal_f.real,
#                             'signal_imag':signal_f.imag}

data_selected_ranges = {'Br':[0,0,-1],'Vr':[0,0,-1]}

max_n = 100#len(di_bbrr['x'])


#----------------------------------------------------------------
# ---------------------- Elements ------------------------------

#-------- Upload File -----------------------------------------
upload_cmp =  Col([dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A(' Select File')
        ],className="text-center m-3 fs-4"),
        className="border border-3 rounded-3 border-primary "+\
                    "bg-primary text-secondary "+\
                    "w-100 h-10 ms-5"  ,
        multiple=False) ],
        width=12,class_name="d-flex justify-content-center mt-3 mb-5")


#---------------- Selectors -------------------------------------
row_selector_b = Row([ 
                     Col([
                        dcc.RangeSlider(id='B-uploaded',
                                    min=0, max=10, step=1, value=[0,10],
                                    marks={i: f'{i}' for i in range(0,10,2)},
                                    ),],width=3,className='mt-3'),
                     Col([
                        dbc.InputGroup([
                            dbc.InputGroupText(["B_min"]),
                            dbc.Input(id="B_min-uploaded",
                                      value=0, debounce=True),
                            #dbc.InputGroupText(["B_sel"]),
                            #dbc.Input(id="B_sel-uploaded",
                            #          value=0,debounce=True),
                            dbc.InputGroupText(["B_max"]),
                            dbc.Input(id="B_max-uploaded", 
                                      value=0,debounce=True),
                        ])],width=3),

    ],class_name='m-2',id='row-selector-b-uploaded')

row_selector_v = Row([ 
                     Col([
                        dcc.Slider(id='V-uploaded',
                                   min=0, max=10, step=1, value=5,
                                      marks={i: f'{i}' for i in range(0,10,2)},
                                    ),],width=3,className='mt-3'),
                     Col([
                        dbc.InputGroup([
                            #dbc.InputGroupText(["V_min"]),
                            #dbc.Input(id="V_min-uploaded",
                            #          value=0,debounce=True),
                            dbc.InputGroupText(["V_sel"]),
                            dbc.Input(id="V_sel-uploaded",
                                      value=0,debounce=True),
                            #dbc.InputGroupText(["V_max"]),
                            #dbc.Input(id="V_max-uploaded", 
                            #          value=0,debounce=True),
                        ])],width=3),

    ],class_name='m-2',id='row-selector-v-uploaded')

#------------------------ buttons --------------------------------
btn_fourier_uploaded = dbc.Button(" Download fft", 
                                  id="btn-fourier-uploaded",
                         n_clicks=0, class_name="fa fa-download mr1")

btn_recon_uploaded = dbc.Button(" Download reconstruction", 
                                id="btn-rec-uploaded",
                         n_clicks=0, class_name="fa fa-download mr1")


#---------------------------- Toggle increasing or decreasing ------------------
toggle =   dbc.Checklist(
            options=[{"label": "Decreasing B values", "value": True}],
            id="toggle-switch-uploaded",
            inline=True,
            switch=True,
            value=[],
        ),

row_toggle = Row([ 
                     Col([
                        html.H3("B values decreasing orders:"),
                        ],width=2),
                     Col([
                        *toggle,
                        ],width=3,align="center"),

    ],class_name='m-2')


#----------------------------- layout parts ------------------------------------


comp_sel_row = Row( [Col([],width=6), 
                     Col([ html.H3("Number of components:"),
                                dcc.Slider(id='n_comps-uploaded',
                                    min   = 1 ,   max  = max_n,
                                    value = 10,   step = 1,
                                    marks={i: f'{i}' 
                                        for i in range(0,max_n,max_n//6)},
                                    tooltip = {'always_visible':True,
                                            'placement':'bottom'}, 
                                    ),],width=6)])

graph_row = Row([ Col([ 
                        dcc.Graph(id='freq-graph-uploaded',
                            figure= fig_freq,className='m-0 '), 
                ],width=6),
                Col([
                   
                    dcc.Graph(id='graph-uploaded',
                        figure=fig,className='m-0 ',
                        ),
                ], width=6),
])                    


data_cmp = dbc.Container([
                dcc.Store(id='data-uploaded', data = {}),
                dcc.Store(id='proc-data-uploaded', data = {}),
                dcc.Store(id= 'selected-freqs-uploaded',  data = []),

                
                ])

#TODO: tengo hecha la vista, me falta agregar la lógica:
"""
1- Parsear los datos para_uli
2- agregar el gráfico de frecuencias y reconstrucción
 """


#plot_row = Row([ 
# #----------------------------------------------------------------
# #-------- buttons Col -----------------------------------------

btns = Row([
            Col([ btn_fourier_uploaded],width=6),
            Col([ btn_recon_uploaded],width=6),
        ])

#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------

layout = dbc.Container([
    data_cmp,
    upload_cmp,
    dbc.Collapse([
        row_toggle,
        row_selector_b,
        row_selector_v,
        comp_sel_row,
        graph_row,
        btns,
        dcc.Download(id="download-uploaded")
    ],id='collapse-uploaded',is_open=False),
],className="h-100 mw-100 container-flex")
    