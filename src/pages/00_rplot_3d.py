import dash_bootstrap_components as dbc
from dash import (dcc, html, register_page)
from dash_bootstrap_components import Col, Row
from dash_bootstrap_templates import load_figure_template

load_figure_template("slate")



#--------------------------------register-----------------------------
register_page(__name__, path="/",name = "3D Plot")
#---------------------------------------------------------------------

from utils import page as pgut
from utils import pajama as utpj


from pages.shared_pajama import shared_pajama


B,V,r = pgut.dd

#------------------------Funciones de figuras------------------------------
f_img = utpj.create_fig_and_cnf()
f_img = utpj.draw_img_trace(f_img,B,V,r)

f_v = utpj.create_fig_and_cnf()
f_v = utpj.draw_Vcte_trace(f_v,B,V,r)


f_b = utpj.create_fig_and_cnf()
f_b = utpj.draw_Bcte_trace(f_b,B,V,r)

"""!IMPORTANT esta función define el orden de los plots, y
si se cambia los callbacks no van a funcionar correctamente. Cuidado 
al tocar."""
#esto me define el orden de los traces
def get_fig_rangedic(B,V,r):
    fig, fig_range_dic = pgut.create_fig_and_cnf(B,V,r)

    fig = pgut.surface_trace(    B, V, r, fig, fig_range_dic  )
    fig = pgut.get_B_cte_traces( B, V, r, fig, fig_range_dic  )
    fig = pgut.get_V_cte_traces( B, V, r, fig, fig_range_dic  )
    fig = pgut.get_r_zqueeze(    B, V, r, fig, fig_range_dic  )
    # [0] superficie
    #[ 1,2,3] B=cte
    #[4,5,6] V=cte
    #[7] R=cte
    return fig,fig_range_dic


fig,fig_range_dic = get_fig_rangedic(B,V,r)

#un comentario nuevo

# def correct_vert_slider_vals(vals,maxVal):
#     vals = [maxVal-i-1 for i in vals][::-1]
#     return vals

def create_idx_rangeslider(id,vec,n_marks=6,unit='',
                           vertical=False,reversed=False):
    n = len(vec)
    st = n//n_marks

    marks = { f"{i}": f"{vec[i]:.2f} {unit}"
        for i in range(0,n,st)}
    min_val = 0
    max_val = n-1
   
    rgslider = dcc.RangeSlider(id=f"rgslider-{id}",
                               className=f"rgslider{id}",
                             min=min_val,
                             max=max_val,
                             value=[min_val,n//2,max_val    ],
                             step=1,
                             marks=marks,
                             vertical=vertical,
                             #updatemode='drag',
                             tooltip={'always_visible':False,}
                             )
    return rgslider



#------------------------Layout----------------------------------------
layout = dbc.Container([
  Row([
    #la primer columna va a tener el plot de antes
    Col([ #la primer fila en esta col tiene el slider y el plot
      Row([ 
        dbc.Col([create_idx_rangeslider("V", V, unit="mV",vertical=True)
            ],width=1, className="d-flex"),
        dbc.Col([dcc.Graph(id="3d-graph", figure=fig,
                           className="h-100 m-0",)#"fig3d",)#
            ],width=11,),  
      ],className="row1-3d"),  
      html.Br(),
      Row([
        dbc.Col([create_idx_rangeslider("B",B,unit="T")], width=12),
      ]),
    ], className="w-50 h-100 ms-0 me-10 border rounded 3 border-dark"),#"col50width"),
    
    #----------------- Segunda columna----------------------------
    # , 
    shared_pajama,
  ]),
],className="mw-100 container-flex" ) #,style= {'height': '75vh','width':'100%'},)
  






