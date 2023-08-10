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


def update_Bcte_val(B, V, r, B_rang, V_rang):
    vv = V[V_rang[0]:V_rang[2]]
    rr = r[V_rang[0]:V_rang[2], B_rang[1]]
    return {'y':vv,'x':rr}


def update_Vcte_val(B,V,r,B_rang,V_rang):
    bb = B[B_rang[0]:B_rang[2]]
    rr = r[V_rang[1],B_rang[0]:B_rang[2]]
    return {'x':bb,'y':rr}

def update_img_val(B,V,r,B_rang,V_rang):
    #print( f"B_rang: {B_rang},")
    bb = B[B_rang[0]:B_rang[2]]
    vv = V[V_rang[0]:V_rang[2]]
    rr = r[V_rang[0]:V_rang[2],B_rang[0]:B_rang[2]]
    #print(f"bb0:{bb[0]}, n: {len(bb)}") 
    im_dic = {'x':bb,'y':vv,'z':rr}
    bcte = {'y':[vv[0],vv[-1]],'x':[B[B_rang[1]],B[B_rang[1]]]}
    vcte = {'x':[bb[0],bb[-1]],'y':[V[V_rang[1]],V[V_rang[1]]]}
    return im_dic,bcte,vcte


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

    return fig

def draw_Vcte_trace(fig,B,V,r):
    n = len(V)//2
    bb = B
    rr = r[n,:]
    fig.add_trace(go.Scatter(x=bb,y=rr,mode='lines',name='Vcte'))
    fig.update_xaxes(autorange="reversed")

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


def tryfloat(val):
    try:
        v = float(val)
    except:
        v = None
    return v