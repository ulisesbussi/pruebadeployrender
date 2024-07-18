import dash_bootstrap_components as dbc
from dash import dcc, html, register_page
from dash_bootstrap_components import Col, Row

from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")


from utils import page as pgut

from pages.shared_pajama import shared_pajama

#--------------------------------register-----------------------------
register_page(__name__, path="/bcte-fourier",name = "B-section Fourier")
#---------------------------------------------------------------------

data = pgut.dd_data

fig,di_vvrr = pgut.trace_b_2d(data)
freq_f,signal_f = pgut.fourier_transform(di_vvrr)
fig_freq = pgut.freq_graph(freq_f,signal_f)

rsig,signals,principal_freqs = pgut.reconstruct_w_n_comps(freq_f,
                                                          signal_f,size=None,n_comps=10)
fig_rec = pgut.draw_reconstruction(di_vvrr['x'],rsig,fig)

data_freq = {'freq':freq_f,'signal_real':signal_f.real,
                            'signal_imag':signal_f.imag}
data_selected_ranges = {'Br':[0,0,-1],'Vr':[0,0,-1]}

max_n = len(di_vvrr['x'])

#----------------------------------------------------------------
#-------- buttons Col -----------------------------------------
btn_fourier_bcte = dbc.Button(" Download fft", id="btn-fourier-bcte",
                         n_clicks=0, className="fa fa-download mr1")

btn_recon_bcte = dbc.Button(" Download reconstruction", id="btn-rec-bcte",
                         n_clicks=0, className="fa fa-download mr1")

btns = Col([ btn_fourier_bcte, btn_recon_bcte,],width=12)

#----------------------------------------------------------------
#--------------------------layout--------------------------------
#----------------------------------------------------------------

layout = dbc.Container([
    Row([
       shared_pajama,
      
       Col([
            dcc.Store(id= 'selected-ranges-bcte', data = data_selected_ranges),
            dcc.Store(id= 'selected-freqs-bcte',  data = []),
            html.H1(" Fourier Transform B constant section",
                        className='title', id='title'),
            dcc.Graph(id='freq-graph-bcte',
                figure= fig_freq,className='m-0 '),
            Row([
                html.H3("Number of components:"),
                dcc.Slider(id='n_comps-bcte',
                                min   = 1 ,   max  = max_n,
                                value = 10,   step = 1,
                                marks={i: f'{i}' 
                                       for i in range(0,max_n,max_n//6)},
                                tooltip = {'always_visible':True,
                                           'placement':'bottom'},   
                          ),
            ]),
            html.Br(className="h-10"),
            dcc.Graph(id='graph-bcte',
                figure=fig,className='m-0 ',
                ),
            Row([ btns], className="w-50 h-10 ms-0 me-10"),
       ],className="w-50 h-100 ms-0 me-10 "),
    ]),
    dcc.Download(id="download-bcte"),
],className="h-100 mw-100 container-flex")

