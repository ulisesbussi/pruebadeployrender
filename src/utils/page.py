
import numpy as np
import pandas as pd
import scipy.fft as fft
from plotly import graph_objs as go
from plotly.subplots import make_subplots

""" funciones auxiliares de todas las páginas, algunas 
están separadas pero otras se utilizan en varios lados. Creo que es 
preferible tenerlas todas juntas acá.
Organizar en detalle todas estas funciones cada una en su módulo
es un trabajo largo. 

Prestar principal atención al hecho de que las figuras de plotly
definen sus propios márgenes y tamaños y no se pueden cambiar desde 
fuera.


"""


#----------- Dataset de Nakamura ----------------
file_name= "41567_2020_1019_MOESM11_ESM.csv"
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
    #Cambio el orden de B y r para que B vaya de menor a mayor
    return B,V_milis,r


def get_BVr2(data_dic):
    """Devuelve B,V,r de un diccionario"""
    B = np.array(data_dic['B'])
    V = np.array(data_dic['V'])
    r = np.array(data_dic['r'])
    return B,V,r


def get_BVr(data_dic=None):
    """Devuelve B,V,r de un diccionario"""
    if data_dic is None:
        B,V,r = dd
    else:
        B = np.array(data_dic['B'])
        V = np.array(data_dic['V'])
        r = np.array(data_dic['r'])
    return B,V,r

#------------------------------------------------------------------

#------------------------------------------------------------------
#---------------------plot 3d functions ---------------------------
#------------------------------------------------------------------
"""Estas funciones son para crear la figura de la primer página y 
actualizarla cuando sea necesario, definen la construcción, colores
datos, etc. La figura 3d tiene 8 componentes:
0- La superficie de los datos graficada en 3d
[1,2,3]- B-constante, grafico en la pared, en la superficie y en el piso
[4,5,6]- V-constante, grafico en la pared, en la superficie y en el piso
7- pajama plot en el piso

"""
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


def get_fig_range_dic(B,V,r):
    rx,ry,rz = get_fig_ranges(B,V,r)
    return {'x':rx,'y':ry,'z':rz}

    
def create_fig_and_cnf(B, V, r):
    "crea la figura y setea los límites de la misma"
    range_x, range_y, range_z = get_fig_ranges(B,V,r)
    
    fig = go.Figure()
    fig.update_layout(
        autosize = True,

        scene = dict(
            xaxis = scene_axis_dict(range_x),
            yaxis = scene_axis_dict(range_y, 
                                              "rgb(230, 200,230)"),
            zaxis = scene_axis_dict(range_z,
                                              "rgb(30, 230,200)"),
            xaxis_title='B [T]',
            yaxis_title='V [mV]',
            
        ),  
        showlegend=False,
        margin=dict( r=0, l=0, b=0, t=0),      
       
        
    )
    return fig ,{'x':range_x,'y':range_y,'z':range_z}

#---- Funciones para obtener diccionarios de lineas, imagenes y surperficies----
#-------------------------------------------------------------------------------
def get_dics_val_b_cte(B,V,r,B_se,V_se, wall_pos):
    bs,be = B_se[::2]
    vs,ve = V_se[::2]
    vals = r[vs:ve, B_se[1]]
    onvl = np.ones_like(vals)
    
    cur_b_val = B[B_se[1]]
    vv = V[vs:ve]
    
    y_plane,z_plane = np.meshgrid(wall_pos['y'],wall_pos['z'])
    x_plane = cur_b_val*np.ones_like(y_plane)
    
    wall = {'x':wall_pos['x'][0]* onvl,
            'y':vv,
            'z':vals}
    surf = {'x':cur_b_val*onvl,
            'y':vv,
            'z':vals}
    floor = {'x':cur_b_val*onvl,
             'y':vv,
             'z':wall_pos['z'][0]*onvl}

    return wall,surf,floor 

def get_dics_val_v_cte(B,V,r,B_se,V_se, wall_pos):
    bs,be = B_se[::2]
    vs,ve = V_se[::2]
    vals = r[V_se[1], bs:be]
    onvl = np.ones_like(vals)
    
    cur_v_val = V[V_se[1]]
    bb = B[bs:be]
    wall = {'x':bb,
            'y':wall_pos['y'][0]*onvl,
            'z':vals}
    surf = {'x':bb,
            'y':cur_v_val*onvl,
            'z':vals}
    floor = {'x':bb,
             'y':cur_v_val*onvl,
             'z':wall_pos['z'][0]*onvl}
    return wall,surf,floor


def get_squeeze_vals(B,V,r,B_se,V_se, wall_pos):
    """devuelve los valores de B,V y r para graficar 
    en el pajama plano en 3d"""
    bs,be = B_se[::2]
    vs,ve = V_se[::2]
    
    bb = B[bs:be]
    vv = V[vs:ve]
    rr = r[vs:ve,bs:be]
    di = {'x':bb,'y':vv,
          'z':wall_pos['z'][0]*np.ones_like(rr),
          'surfacecolor':rr} 
    return di

def get_surf_vals(B,V,r,B_se,V_se):
    bs,be = B_se[::2]
    vs,ve = V_se[::2]
    di = {'x':B[bs:be],
          'y':V[vs:ve],
          'z':r[vs:ve,bs:be]} #primero fila luego col
    return di
#-------------------------------------------------------------------------------



#---- Funciones que generan trazas ----------------------
"""Esto sigue siendo parte del gráfico 3d, genera las trazas,
es decir los gráficos en si, las de arriba solo genera los diccionarios
Este los convierte en plots."""
def surface_trace(B, V, r, fig, ranges):
    """Genera la superficie para el plot"""
    
    fig.add_surface(x=B, y=V, z=r,
                    colorscale='jet',
                    colorbar=dict(
                        title=r"&#916;G <sup> e<sup>2</sup></sup>/<sub>h</sub>",#"\delta G \[e^2/h\]",
                        lenmode='fraction',
                        len=0.7,
                        ),              
    )
    
    return fig


def get_B_cte_traces(B, V, r, fig, wall_pos):
    """crea las 3 trazas INICIALES relacionadas a B=cte"""
    nb,nv = len(B), len(V)
    dic_list = get_dics_val_b_cte(B,V,r,
                                  [0,nb//2,nb],
                                  [0,nv//2,nv],
                                  wall_pos)
    names = ['B proy','B surf','B floor']
    for di,name in zip(dic_list[:3],names):
        fig.add_trace(go.Scatter3d(**di,
                                   mode='lines',
                                   ))#name=name))
        fig.data[-1].update(line=dict(color='black', width=10))
   
    return fig


def get_V_cte_traces(B, V, r, fig, wall_pos):
    """crea las 3 trazas relacionadas a V=cte"""
    nb,nv = len(B), len(V)
    dic_list = get_dics_val_v_cte(B,V,r,
                                  [0,nb//2,nb],
                                  [0,nv//2,nv],
                                  wall_pos)
    names = ['V proy','V surf','V floor']
    for di,name in zip(dic_list,names):
        fig.add_trace(go.Scatter3d(**di,
                                   mode='lines',
                                   ))#name=name))
        fig.data[-1].update(line=dict(color='black', width=10))
    return fig


def get_r_zqueeze(B,V,r,fig, wall_pos):
    """crea las sombra de R como imagen en el piso"""
    nb,nv = len(B), len(V)
    di = get_squeeze_vals(B,V,r,
                          [0,nb//2,nb],
                          [0,nv//2,nv],
                          wall_pos)
    fig.add_trace(go.Surface(**di,
                             #surfacecolor=r,
                             cmin=r.min(),
                             cmax=r.max(),
                             colorscale='jet',
                             showscale=False,
                )
    )
    fig.update_xaxes(autorange="reversed")
    return fig


#-------------------------------------------------------------------------------
#funcion que recorta los datos originales a los rangos propuestos.
#no estoy seguro para que uso esta función... 
#quiza se pueda eliminar y forme parte de algun elemento temporal removido
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
#estas funciones actualizan las figuras a partir de Patch de dash.
#de esta forma no se vuelve a generar la figura sino que se "cambia"
#Esto ahorra tiempo a la hora de actualizar los gráficos.
def update_Vcte_val(B, V, r, 
                    patched_fig,
                    B_se=None,
                    V_se=None,
                    wall_pos={}):

    traces_v_dic = get_dics_val_v_cte(B,V,r,B_se,V_se,wall_pos)
    traces_indices = [4,5,6]
    for tr_di,trace_index in zip(traces_v_dic,traces_indices):
        patched_fig.data[trace_index].update(tr_di)
    return patched_fig

def update_Bcte_val(B, V, r, 
                    patched_fig,
                    B_se=None,
                    V_se=None,
                    wall_pos={}):
    
    traces_vals = get_dics_val_b_cte(B,V,r,B_se,V_se,wall_pos)
    traces_indices = [1,2,3]
    for tr_di,trace_index in zip(traces_vals[:3],traces_indices):
        patched_fig.data[trace_index].update(tr_di)
    return patched_fig


def update_surf_trace(B, V, r, patched_fig,
                      B_se=None,V_se=None,
                      wall_pos={}):
    srf_vals = get_surf_vals(B,V,r,B_se,V_se)

    patched_fig.data[0].update(srf_vals)
    return patched_fig

def update_squeeze_val(B,V,r, patched_fig,
                       B_se=None,V_se=None,
                       wall_pos={}):
    squeeze_vals = get_squeeze_vals(B,V,r,B_se,V_se,wall_pos)
    patched_fig.data[7].update(squeeze_vals)
    return patched_fig

#-------------------Fin de funciones de 3d-graph ------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------




#-----------Funciones 01_spectral-----------------------------------------------
#-------------------------------------------------------------------------------
#data es un diccionario con las siguientes keys:
#   ['B', 'V', 'r']

def get_selected_ranges(selected_ranges=None):
    """Obtiene B y V en los rangos seleccionados, 
    es una función interna. """
    if selected_ranges is None:
        B_rang= [0,0,-1]
        V_rang= [0,0,-1]
    else:
        B_rang = selected_ranges.get('Br',[0,0,-1])
        V_rang = selected_ranges.get('Vr',[0,0,-1])
    return B_rang,V_rang

def BVr_array(data):
    """Los Store de dash guardan o listas o diccionarios, 
    no np.ndarrays asi que convierto para utilizar"""
    B = np.array(data['B'])
    V = np.array(data['V'])
    r = np.array(data['r'])
    return B,V,r


def get_b_trace(data,selected_ranges=None):
    "obtengo la traza plana con b=cte"
    if data=={}:
        return {'x':[],'y':[]}
    B_rang,V_rang = get_selected_ranges(selected_ranges)
    B,V,r = BVr_array(data)
    B_val = B_rang[1]
    vs,ve = V_rang[::2]
    vv = V[vs:ve]
    rr = r[vs:ve,B_val]
    return {'x':vv,'y':rr}

def get_v_trace(data,selected_ranges=None):
    "idem get_b_trace pero con v=cte"
    if data=={}:
        return {'x':[],'y':[]}
    B_rang,V_rang = get_selected_ranges(selected_ranges)

    B,V,r = BVr_array(data)
    V_val = V_rang[1]
    bs,be= B_rang[::2]
    bb = B[bs:be]
    rr = r[V_val,bs:be]
    return {'x':bb,'y':rr}

def trace_b_2d(data,selected_ranges=None):
    "creo la figura de la traza"
    fig = go.Figure()
    fig['layout'].update(margin=(dict(t=10,b=10,l=10)),
                         autosize =True ,height=300)
    if data=={}:
        return fig, {}
    di = get_b_trace(data,selected_ranges)
    fig.add_trace(go.Scatter(di,name='B trace'))
    fig.data[-1].update(line=dict(color="#0063db"))
    return fig, di

def trace_v_2d(data,selected_ranges=None):
    "creo la figura de la traza"
    fig = go.Figure()
    fig['layout'].update(margin=(dict(t=10,b=10,l=10)),
                         autosize =True ,height=300)
    if data=={}:
        return fig, {}
    di = get_v_trace(data,selected_ranges)
    fig.add_trace(go.Scatter(di,name='V trace'))
    fig.data[-1].update(line=dict(color="#0063db"))
    return fig, di

def fourier_transform(di):
    """calculo la transformada de fourier. Calcula la transformada
    de fourier real, esto permite tener solo las freqs positivas
    y facilitar la reconstrucción."""
    xx = di['x']
    yy = di['y']
    if not len(xx):
        return [],[]
    signal_f = fft.rfft(yy)
    freq_f = fft.rfftfreq(len(xx),xx[1]-xx[0])
    return -freq_f,signal_f 


def get_freq_data(freq_f,signal_f):
    """separo en norma y fase para graficar"""
    return {0:{'x':freq_f,'y':np.abs(signal_f)},
            1:{'x':freq_f,'y':np.angle(signal_f)}}


def freq_graph(freq_f,signal_f):
    """Creo el gráfico"""
    freq_data = get_freq_data(freq_f,signal_f)
    fig = make_subplots(rows=2,cols=1, vertical_spacing=0.1 )
    fig['layout'].update(margin=dict(t=10,b=10,l=10), height=300)
    if len(freq_f):
        fig.add_trace(go.Scatter(freq_data[0],name='amplitude'),row=1,col=1)
        fig.data[-1].update(line=dict(color="#0063db"))
        fig.add_trace(go.Scatter(freq_data[1],name='phase'),row=2,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, 
                                 mode='markers',
                                 marker_color='rgba(250, 0, 0, .8)',
                                 name="selected points"),row=1,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, name='', mode='markers'),row=2,col=1)
    else:
        fig.add_trace(go.Scatter({'x':[],'y':[]},name='amplitude'),row=1,col=1)
        fig.data[-1].update(line=dict(color="#0063db"))
        fig.add_trace(go.Scatter({'x':[],'y':[]},name='phase'),row=2,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, 
                                 mode='markers',
                                 marker_color='rgba(250, 0, 0, .8)',
                                 name="selected points"),row=1,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, name='', mode='markers'),row=2,col=1)
    return fig

def freq_graph2(freq_f,signal_f):
    """Creo el gráfico"""
    freq_data = get_freq_data(freq_f,signal_f)
    fig = make_subplots(rows=2,cols=1, vertical_spacing=0.1 )
    fig['layout'].update(margin=dict(t=10,b=10,l=10), height=300)
    if len(freq_f):
        fig.add_trace(go.Scatter(freq_data[0],name='amplitude'),row=1,col=1)
        fig.data[-1].update(line=dict(color="#0063db"))
        fig.add_trace(go.Scatter(freq_data[1],name='phase'),row=2,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, 
                                 mode='markers',
                                 marker_color='rgba(250, 0, 0, .8)',
                                 name="selected points"),row=1,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, name='', mode='markers'),row=2,col=1)
    else:
        fig.add_trace(go.Scatter({'x':[],'y':[]},name='amplitude'),row=1,col=1)
        fig.data[-1].update(line=dict(color="#0063db"))
        fig.add_trace(go.Scatter({'x':[],'y':[]},name='phase'),row=2,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, 
                                 mode='markers',
                                 marker_color='rgba(250, 0, 0, .8)',
                                 name="selected points"),row=1,col=1)
        fig.add_trace(go.Scatter({'x':[],'y':[]}, name='', mode='markers'),row=2,col=1)
    return fig

def reconstruct_w_n_comps(freq_f,signal_f,size,n_comps=10):
    #reconstruye la señal con las n_comps de mayor amplitud.
    if not len(freq_f):
        return [],[],[]
    principal_freqs = np.argsort(np.abs(signal_f))[-n_comps:]
    components = []
    signals    = []
    n = len(freq_f)
    n_comps = min(n_comps,n) #check if n_comps is grater than n..
    for i in range(n_comps):
        v = np.zeros_like(signal_f)
        v[principal_freqs[i]] = signal_f[principal_freqs[i]]
        components.append(v)
        signals.append(fft.irfft(v,n=size))
    rsig = fft.irfft(sum(components),n=size)
    return rsig,signals,principal_freqs


def reconstruct_w_selected(freq_f,signal_f,selected_freqs,size):
    #reconstruye con frecuencias seleccionadas en el plot
    if not len(freq_f):
        return [],[],[]
    components=[]
    signals=[]
    for val in selected_freqs:
        v = np.zeros_like(signal_f)
        v[val] = signal_f[val]
        components.append(v)
        signals.append(fft.irfft(v,n=size))
    rsig = fft.irfft(sum(components),n=size)
    return rsig,signals,selected_freqs
    

def draw_reconstruction(bb,rsig,fig):
    #dibuja la reconstrucción sobre la figura de entrada.
    if not len(bb):
        return fig
    fig.add_trace(go.Scatter(x=bb,y=rsig,name='Reconstruction'))
    return fig

#%% slider de frecuencias
def update_freq_comp_slider(n):
    max_n = n
    value = min(10,n)
    marks={i: f'{i}' for i in range(0,max_n,max_n//6)}
    return max_n,value,marks

#%%




def update_freq_fig_selected(clickData,selected_points,
                             freq_f,signal_f,freq_fig_patched):
    """checkea los clicks para ver que estén sobre la amp de fourier o 
    los puntos ya creados, si están en amp lo agrega, si está en los ya
    agregados lo quita.
    Y por último actualiza la figura con Patch
    """
    curveNumber = clickData['points'][0]['curveNumber']
    if curveNumber not in [0,2]:
        return freq_fig_patched,selected_points
    idx = clickData['points'][0]['pointIndex']
    if curveNumber == 0:
        if idx in selected_points:
            selected_points.remove(idx)
        else:
            selected_points.append(idx)
    else:
        selected_points.pop(idx)
    
    di= {'x': freq_f[selected_points],'y':np.abs(signal_f[selected_points])}
    freq_fig_patched.data[2].update(di)
    return freq_fig_patched,selected_points


#%%


def download_fourier(freq,signal,data,selected_ranges, vcte=True):
    """genera el archivo de descarga de la transformada de fourier"""
    df = pd.DataFrame({'freq':freq,'signal_real':signal.real,
                       'signal_imag':signal.imag})
    B = data['B']
    V = data['V']
    B_rang = selected_ranges.get('Br',[0,0,-1])
    V_rang = selected_ranges.get('Vr',[0,0,-1])
    if vcte:
        start = B[B_rang[0]]
        end = B[B_rang[2]]
        current = V[V_rang[1]]
        constant = 'V'
        variable = 'B'
    else:
        start = V[V_rang[0]]
        end = V[V_rang[2]]
        current = B[B_rang[1]]
        constant = 'B'
        variable = 'V'
        
    name = f"fourier_{constant}cte_{current:.3f}_{variable}_from_{start:.3f}_to_{end:.3f}.csv"
    
    return df.to_csv , name

"""51 min """

def download_reconstruction(xx,rsig,comp_freqs,sel_freqs,vcte=True):
    
    partial = {f:v for f,v in zip(sel_freqs,comp_freqs)}
    x = 'B' if vcte else 'V'
    csv =pd.DataFrame({x:xx,'reconstruction':rsig,**partial},index=None).to_csv
    if vcte:
        name = "reconstruction_Vcte.csv"
    else:
        name = "reconstruction_Bcte.csv"
    return csv,name
    


#%%
#-------------------------------- Data definition



dd = get_dataset()
B,V,r = dd
wall_pos = get_fig_range_dic(B,V,r)
dd_data = {'B':B.tolist(),'V':V.tolist(),'r':r.tolist(), 
            'wall_pos':wall_pos}

