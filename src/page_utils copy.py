import os
import pandas as pd
import numpy as np
from plotly import graph_objs as go
from dash import Patch

#----------- Dataset de Nakamura ----------------
file_name= "../41567_2020_1019_MOESM11_ESM.csv"

#---------------------Dataset functions------------------------------
def get_dataset():
    """Devuelve los datos de la tabla de datos de Nakamura
    Retorna B,V,r"""
    st = 3
    end = 270
    df = pd.read_csv(file_name, 
                     skiprows=st, 
                     nrows=end-st,
                    )

    B = np.array(list(df.keys())[1:],dtype=float)
    V = df['Unnamed: 0'].values
    V_milis = V*1000
    df.drop(columns=['Unnamed: 0'],inplace=True)
    r = df.values
    return B,V_milis,r
#------------------------------------------------------------------


#------------------------------------------------------------------
#---------------------plot 3d functions ---------------------------
#------------------------------------------------------------------
def scene_axis_dict(range,bg_col = "rgb(200,200,230)"):
    #crea el axis_dict que tiene información de color de las paredes    
    di = dict(
        backgroundcolor=bg_col,
        gridcolor="black",
        showbackground=True,
        range=range,
        )
    return di


def get_fig_ranges(B,V,r,k=0.3,B_se=[0,-1],
                   V_se=[0,-1]):
    """calcula los limites de la imagen y los devuelve"""
    B = B[B_se[0]:B_se[1]]
    V = V[V_se[0]:V_se[1]]
    r = r[V_se[0]:V_se[1],B_se[0]:B_se[1]]
    min_x,max_x = B.min(),B.max()
    min_y,max_y = V.min(),V.max()
    min_z,max_z = r.min(),r.max()
    range_x = [min_x - k*(max_x - min_x), max_x + k*(max_x - min_x)]
    range_y = [min_y - k*(max_y - min_y), max_y + k*(max_y - min_y)]
    range_z = [min_z - k*(max_z - min_z), max_z + k*(max_z - min_z)]
    return range_x,range_y,range_z



    
def create_fig_and_cnf(B, V, r):
    "crea la figura y setea los límites de la misma"
    range_x, range_y, range_z = get_fig_ranges(B,V,r)
    
    fig = go.Figure()
    fig.update_layout(
        autosize = False,
  
        scene = dict(
            xaxis = scene_axis_dict(range_x),
            yaxis = scene_axis_dict(range_y, 
                                              "rgb(230, 200,230)"),
            zaxis = scene_axis_dict(range_z,
                                              "rgb(30, 230,200)"),
            xaxis_title='B [T]',
            yaxis_title='V [mV]',
            
        ),        
        margin=dict( r=10, l=10, b=10, t=10),
        height = 700,
        legend=dict(orientation='h',yanchor='bottom',
                    xanchor='center',y=1,x=0.5)
    )
    return fig ,{'x':range_x,'y':range_y,'z':range_z}
#---- Funciones para obtener diccionarios de lineas, imagenes y surperficies----
#-------------------------------------------------------------------------------
def get_dics_val_b_cte(B,V,r,idx,ranges):
    vals = r[:,idx]
    onvl = np.ones_like(vals)
    wall = {'x':ranges['x'][0]* onvl,
            'y':V,
            'z':vals}
    surf = {'x':B[idx]*onvl,
            'y':V,
            'z':vals}
    floor = {'x':B[idx]*onvl,
             'y':V,
             'z':ranges['z'][0]*onvl}
    return wall,surf,floor

def get_dics_val_v_cte(B,V,r,idx,ranges):
    vals = r[idx,:]
    onvl = np.ones_like(vals)
    wall = {'x':B,
            'y':ranges['y'][0]* onvl,
            'z':vals}
    surf = {'x':B,
            'y':V[idx]*onvl,
            'z':vals}
    floor = {'x':B,
             'y':V[idx]*onvl,
             'z':ranges['z'][0]*onvl}
    return wall,surf,floor

def get_squeeze_vals(B,V,r,ranges):
    di = {'x':B,'y':V,
          'z':ranges['z'][0]*np.ones_like(r)}
    return di

def get_surf_vals(B,V,r,ranges):
    di = {'x':B,'y':V,'z':r}
    return di
#-------------------------------------------------------------------------------



#---- Funciones que generan trazas ----------------------

def surface_trace(B, V, r, fig, ranges):
    """Genera la superficie para el plot"""
    fig.add_surface(x=B, y=V, z=r,
                    colorscale='jet',
                    name = 'surface',
                    colorbar=dict(
                        title="\delta G \[e^2/h\]",
                        lenmode='fraction',
                        len=0.7,
                        ),              
    )
    return fig


def get_B_cte_traces(B, V, r, fig, ranges, idx):
    """crea las 3 trazas relacionadas a B=cte"""
    dic_list = get_dics_val_b_cte(B,V,r,idx,ranges)
    names = ['B proy','B surf','B floor']
    for di,name in zip(dic_list,names):
        fig.add_trace(go.Scatter3d(**di,
                                   mode='lines',
                                   name=name))
        fig.data[-1].update(line=dict(color='black', width=10))
    return fig


def get_V_cte_traces(B, V, r, fig, ranges, idx):
    """crea las 3 trazas relacionadas a V=cte"""
    dic_list = get_dics_val_v_cte(B,V,r,idx,ranges)
    names = ['V proy','V surf','V floor']
    for di,name in zip(dic_list,names):
        fig.add_trace(go.Scatter3d(**di,
                                   mode='lines',
                                   name=name))
        fig.data[-1].update(line=dict(color='black', width=10))
    return fig


def get_r_zqueeze(B, V, r, fig, ranges):
    """crea las sombra de R como imagen en el piso"""
    di = get_squeeze_vals(B,V,r,ranges)
    fig.add_trace(go.Surface(**di,
                             surfacecolor=r,
                             cmin=r.min(),
                             cmax=r.max(),
                             colorscale='jet',
                             showscale=False,
                )
    )
    return fig

#-------------------------------------------------------------------------------


def slice_data(B,V,r,B_se=None,V_se=None):
    if B_se is None:
        B_se = [0,-1]
    if V_se is None:
        V_se = [0,-1]
    BB = B[B_se[0]:B_se[1]] #recorto los originales
    VV = V[V_se[0]:V_se[1]]
    rr = r[V_se[0]:V_se[1],B_se[0]:B_se[1]]
    return BB,VV,rr
    

#---------- Funciones de updates -----------------------------------------------

def update_Vcte_val(B, V, r, v_val, patched_fig, range_dic):

    traces_v_dic = get_dics_val_v_cte(B,V,r,v_val,range_dic)
    traces_indices = [4,5,6]
    for tr_di,trace_index in zip(traces_v_dic,traces_indices):
        patched_fig.data[trace_index].update(tr_di)
    return patched_fig

def update_Bcte_val(B, V, r, b_bal, patched_fig, range_dic):
    traces_b_dic = get_dics_val_b_cte(B,V,r,b_bal,range_dic)
    traces_indices = [1,2,3]
    for tr_di,trace_index in zip(traces_b_dic,traces_indices):
        patched_fig.data[trace_index].update(tr_di)
    return patched_fig

def update_surf_trace(B, V, r, patched_fig, range_dic,
                      V_se=None,B_se=None):

    B, V, r = slice_data(B,V,r, B_se, V_se)
    srf_vals = get_surf_vals(B,V,r,range_dic)

    patched_fig.data[0].update(srf_vals)
    return patched_fig,(B,V,r)

