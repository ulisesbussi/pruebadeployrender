import os
import pandas as pd
import numpy as np
from plotly import graph_objs as go
from dash import Patch
import json
import scipy.fft as fft
from plotly.subplots import make_subplots
import os

#--------------------------------------

def create_fig_and_cnf():
    "crea la figura y setea los límites de la misma"
    
    fig = go.Figure()
    fig.update_layout(
        autosize = True,
  
        showlegend=False,
        margin=dict( r=0, l=0, b=0, t=0),      
    )
        
    return fig 


#--------------------------------------
#Dics
def update_Bcte_val(B, V, r, B_rang, V_rang,vertical=True):
    #on pajama is a vertical plot but i might want it as horizontal 
    vv = V[V_rang[0]:V_rang[2]]
    rr = r[V_rang[0]:V_rang[2], B_rang[1]]
    if vertical:
        return {'y':vv,'x':rr}
    else:
        return {'x':vv,'y':rr}


def update_Vcte_val(B,V,r,B_rang,V_rang,vertical=False):
    bb = B[B_rang[0]:B_rang[2]]
    rr = r[V_rang[1],B_rang[0]:B_rang[2]]
    if vertical:
        return {'y':bb,'x':rr}
    else:
        return {'x':bb,'y':rr}



def update_img_val(B,V,r,B_rang,V_rang):
    bb = B[B_rang[0]:B_rang[2]]
    vv = V[V_rang[0]:V_rang[2]]
    rr = r[V_rang[0]:V_rang[2],B_rang[0]:B_rang[2]]
    im_dic = {'x':bb,'y':vv,'z':rr}
    bcte = {'y':[vv[0],vv[-1]],'x':[B[B_rang[1]],B[B_rang[1]]]}
    vcte = {'x':[bb[0],bb[-1]],'y':[V[V_rang[1]],V[V_rang[1]]]}
    return im_dic,bcte,vcte


def get_cte_trace_df(data,B_rang,V_rang,vcte=True):
    B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
    
    if vcte:
        di =update_Vcte_val(B,V,r,B_rang,V_rang)
        sval  = V[V_rang[1]]
        start = B[B_rang[0]]
        end   = B[B_rang[2]]
        tr = 'V'
        x  = 'B'
    else:
        di =update_Bcte_val(B,V,r,B_rang,V_rang)
        sval  = B[B_rang[1]]
        start = V[V_rang[0]]
        end   = V[V_rang[2]]
        tr = 'B'
        x  = 'V'
    otp_csv = pd.DataFrame({x:di['x'],'r':di['y']},
                           index=None).to_csv(sep=',')

    csv_name = f'{tr}cte_{sval:.3f}_from_{x}_{start:.3f}_to_{end:.3f}.csv'
    return pd.DataFrame({x:di['x'],'r':di['y']},
                           index=None),csv_name


def get_img_df(data,B_rang,V_rang):
    B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
    bb = B[B_rang[0]:B_rang[2]]
    vv = V[V_rang[0]:V_rang[2]]
    rr = r[V_rang[0]:V_rang[2],B_rang[0]:B_rang[2]]
    df = pd.DataFrame(rr,index=vv,columns=bb)
    csv_name = f'data_from_B_{bb[0]:.3f}_to_{bb[-1]:.3f}_V_{vv[0]:.3f}_to_{vv[-1]:.3f}.csv'
    return df, csv_name
# --------------------------------------
# traces

def update_Bcte_trace(fig,bcte_dic):
    fig.data[0].update(bcte_dic)
    return fig

def update_Vcte_trace(fig,vcte_dic):
    fig.data[0].update(vcte_dic)
    return fig

def update_img_trace(fig,img_dic):
    for i,di in enumerate(img_dic):
        fig.data[i].update(di)
    return fig


def draw_Bcte_trace(fig,B,V,r):
    n = len(B)//2
    vv = V
    rr = r[:,n]
    fig.add_trace(go.Scatter(y=vv,x=rr,mode='lines',name='Bcte'))
    fig.update_xaxes(autorange="reversed")
    fig.data[-1].update(line=dict(color="#0063db"))
    return fig

def draw_Vcte_trace(fig,B,V,r):
    n = len(V)//2
    bb = B
    rr = r[n,:]
    fig.add_trace(go.Scatter(x=bb,y=rr,mode='lines',name='Vcte'))
    fig.update_xaxes(autorange="reversed")
    fig.data[-1].update(line=dict(color="#0063db"))
    return fig


def draw_img_trace(fig,B,V,r):
    nB = len(B)//2
    nV = len(V)//2
    heatmap = go.Heatmap(z=r, x=B, y=V, colorscale='jet')  # Crear el heatmap
    
    fig.add_trace(heatmap) 
    #add line with Bcte and Vmin Vmax
    fig.add_trace(go.Scatter(y=[V[0],V[-1]],x=[B[nB],B[nB]],
                             mode='lines'))
    fig.data[-1].update(line=dict(color='black', width=4))
    fig.add_trace(go.Scatter(y=[V[nV],V[nV]],x=[B[0],B[-1]],
                                mode='lines'))
    fig.data[-1].update(line=dict(color='black', width=4))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(autorange="reversed")
    return fig


#intento convertir string a flotante.
#aca podría haber usado numero en el input pero no me gustaba 
#la visualización con los botones de selector.
def tryfloat(val):
    try:
        v = float(val)
    except:
        v = None
    return v

def update_slider_vals(vals,min,sel,max):
    
    from dash import no_update
    
    min = tryfloat(min)
    sel = tryfloat(sel)
    max = tryfloat(max)
    new_rg = np.array([min,sel,max])
    if None in new_rg:
        return no_update
    if (np.diff(new_rg)<0).any(): #improper range
        return no_update
    
    idxs = np.argmin(np.abs(vals[:,None]-new_rg),axis=0)[::-1]
    #vals is a decreasing array, so inverting value order
    #and check that indices are sorted.
    if (np.diff(idxs)<0).any():
        return no_update
    return idxs #idxs[-1]
    

def update_b_inputs(B,B_rang):
    #change bm and bM
    bm = f"{B[B_rang[2]]:.4f}" 
    bs = f"{B[B_rang[1]]:.4f}"
    bM = f"{B[B_rang[0]]:.4f}" 
    return bm,bs,bM

def update_v_inputs(V,V_rang):
    #change vm and vM
    vm = f"{V[V_rang[2]]:.2f}" 
    vs = f"{V[V_rang[1]]:.2f}"
    vM = f"{V[V_rang[0]]:.2f}" 
    return vm,vs,vM