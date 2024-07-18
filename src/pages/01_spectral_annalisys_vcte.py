import dash_bootstrap_components as dbc
from dash import dcc, html, register_page
from dash_bootstrap_components import Col, Row

from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")


from utils import page as pgut

from pages.shared_pajama import shared_pajama

#--------------------------------register-----------------------------
register_page(__name__, path="/vcte-fourier",name = "V-section Fourier")
#---------------------------------------------------------------------

data = pgut.dd_data


fig,di_bbrr = pgut.trace_v_2d(data)
freq_f,signal_f = pgut.fourier_transform(di_bbrr)
fig_freq = pgut.freq_graph(freq_f,signal_f)

rsig,signals,principal_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                          signal_f,size=None,n_comps=10)
fig_rec = pgut.draw_reconstruction(di_bbrr['x'],rsig,fig)

data_freq = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}
data_selected_ranges = {'Br':[0,0,-1],'Vr':[0,0,-1]}

max_n = len(di_bbrr['x'])

#----------------------------------------------------------------
#-------- buttons Col -----------------------------------------
btn_fourier_vcte = dbc.Button(" Download fft", id="btn-fourier-vcte",
                         n_clicks=0, className="fa fa-download mr1")

btn_recon_vcte = dbc.Button(" Download reconstruction", id="btn-rec-vcte",
                         n_clicks=0, className="fa fa-download mr1")

btns = Col([ btn_fourier_vcte, btn_recon_vcte,],width=12)

#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------

layout = dbc.Container([
    Row([
       shared_pajama,
      
       Col([
            dcc.Store(id= 'selected-ranges-vcte', data = data_selected_ranges),
            dcc.Store(id= 'selected-freqs-vcte',  data = []),
            html.H1(" Fourier Transform V constant section",
                            className='title', id='title'),
            dcc.Graph(id='freq-graph-vcte',
                figure= fig_freq,className='m-0 '),
            Row([
                html.H3("Number of components:"),
                dcc.Slider(id='n_comps-vcte',
                                min   = 1 ,   max  = max_n,
                                value = 10,   step = 1,
                                marks={i: f'{i}' 
                                       for i in range(0,max_n,max_n//6)},
                                tooltip = {'always_visible':True,
                                           'placement':'bottom'}, 
                            ),
            ]),
            html.Br(className="h-10"),
            dcc.Graph(id='graph-vcte',
                figure=fig,className='m-0 ',
                ),
            Row([ btns], className="w-50 h-10 ms-0 me-10"),
       ],className="w-50 h-100 ms-0 me-10 "),
    ]),
    dcc.Download(id="download-vcte"),
],className="h-100 mw-100 container-flex")
        
