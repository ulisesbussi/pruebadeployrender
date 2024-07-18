
from dash import (dcc,
    Input,Output,State,callback,
    ALL,ctx,no_update, Patch, no_update

)

import numpy as np

from utils import page as pgut
from utils import pajama as utpj


#Callbacks asociados a la subpagina de pajama plot

#estas funciones de lógica no están en utils porque ya devuelven
#valores propios de dash, como lo son no_update y ctx


# Acá modifiqué todas las funciones para no usar el state shared-data
#de esta forma se ahorra tiempo de procesamiento (envío desde user a server)
# si los datos no fueran fijos tendria que volver a agregar ese estado



# @callback(
#            Output("vcte-pajama", "figure"),
#            Output("img-graph",   "figure"),
#            Output("bcte-pajama", "figure"),
           
#            Input("rgslider-b-pajama", "value"),
#            Input("rgslider-v-pajama", "value"),
           
       
#            prevent_initial_call=True,
#           )
# def update_pajama(B_rang,V_rang):
#     """Este callback se encarga de modificar los graficos del pajama plot
#     tanto la imagen con las lineas, así como las secciones constantes mostradas
#     a izquierda y derecha"""
#     B,V,r = pgut.dd
  
#     bcte_dic     = utpj.update_Bcte_val(B,V,r,B_rang,V_rang)
#     patched_bcte = Patch()
#     patched_bcte = utpj.update_Bcte_trace(patched_bcte,bcte_dic)
#     vcte_dic     = utpj.update_Vcte_val(B,V,r,B_rang,V_rang)
#     patched_vcte = Patch()
#     patched_vcte = utpj.update_Vcte_trace(patched_vcte,vcte_dic)
#     patched_img  = Patch()
#     img_dic      = utpj.update_img_val(B,V,r,B_rang,V_rang)
#     patched_img  = utpj.update_img_trace(patched_img,img_dic)
    
#     return patched_vcte, patched_img, patched_bcte
   


# @callback(
#            Output("vcte-pajama", "figure"),
#            Output("bcte-pajama", "figure"),
           
#            Input("rgslider-b-pajama", "value"),
#            Input("rgslider-v-pajama", "value"),
           
       
#            prevent_initial_call=True,
#           )
# def update_pajama(B_rang,V_rang):
#     """Este callback se encarga de modificar los graficos del pajama plot
#     tanto la imagen con las lineas, así como las secciones constantes mostradas
#     a izquierda y derecha"""
#     B,V,r = pgut.dd
  
#     bcte_dic     = utpj.update_Bcte_val(B,V,r,B_rang,V_rang)
#     patched_bcte = Patch()
#     patched_bcte = utpj.update_Bcte_trace(patched_bcte,bcte_dic)
#     vcte_dic     = utpj.update_Vcte_val(B,V,r,B_rang,V_rang)
#     patched_vcte = Patch()
#     patched_vcte = utpj.update_Vcte_trace(patched_vcte,vcte_dic)
    
#     return patched_vcte, patched_bcte
 
from dash import clientside_callback,ClientsideFunction
  
clientside_callback(
    ClientsideFunction(
        namespace='clientside_pajama_img',
        function_name='update_img_pajama'
    ),
    Output('img-graph', 'figure'),
    #Output('bcte-pajama', 'figure'),
    #Output('vcte-pajama', 'figure'),
    
    Input('rgslider-b-pajama', 'value'),
    Input('rgslider-v-pajama', 'value'),
    State('shared-data', 'data'),
    State('img-graph', 'figure'),
    #State('bcte-pajama', 'figure'),
    #State('vcte-pajama', 'figure'),
    prevent_initial_call=True
)


clientside_callback(
    ClientsideFunction(
        namespace='clientside_pajama_img',
        function_name='update_pajama_b_trace'
    ),
    Output('bcte-pajama', 'figure'),
    
    Input('rgslider-b-pajama', 'value'),
    Input('rgslider-v-pajama', 'value'),
    State('shared-data', 'data'),
    State('bcte-pajama', 'figure'),
    prevent_initial_call=True
)

clientside_callback(
    ClientsideFunction(
        namespace='clientside_pajama_img',
        function_name='update_pajama_v_trace',
    ),
    Output('vcte-pajama', 'figure'),
    
    Input('rgslider-b-pajama', 'value'),
    Input('rgslider-v-pajama', 'value'),
    State('shared-data', 'data'),
    State('vcte-pajama', 'figure'),
    prevent_initial_call=True
)

#%% Callbacks que modifican los sliders e inputs
"""en esta parte tuve que separar los callbacks, dado que algunos 
elementos no están presenten en una página y otra sí. Un callback general
Trae problemas con los elementos que no están presentes."""


@callback(Output("rgslider-b-pajama", "value",allow_duplicate=True),          
          Input("Bmin", "value"),Input("Bsel", "value"),Input("Bmax", "value"),
          State("rgslider-b-pajama", "value"),
          prevent_initial_call=True)
def update_b_slider(min,sel,max,vval):
    """Modifico el slider de B en el pajama plot 
    con los valores de los inputs si se modifican"""
    B,_,_ = pgut.dd
    rg_val = utpj.update_slider_vals(B,min,sel,max)
    return rg_val


@callback(Output("Bmin", "value",allow_duplicate=True),
          Output("Bsel", "value",allow_duplicate=True),
          Output("Bmax", "value",allow_duplicate=True),
          Input("rgslider-b-pajama", "value"),
          prevent_initial_call=True)
def update_b_inputs(B_rang):
    """Modifico los inputs de B en el pajama plot si se modifica el slider"""
    B,_,_ = pgut.dd
    return utpj.update_b_inputs(B,B_rang)
   

@callback(Output("rgslider-b-pajama", "value",allow_duplicate=True),
          Input("rgslider-B", "value"),
          prevent_initial_call=True)
def update_pajama_B_range(B_rang):
    """modifico el pajama  b slider si se modifica el 3d slider de B"""
    return B_rang


@callback(Output("rgslider-B", "value",allow_duplicate=True),
          Input("rgslider-b-pajama", "value"),
            prevent_initial_call=True)
def update_B_range(B_rang):
    """modifico el 3d slider de B si se modifica el pajama b slider"""
    return B_rang

## Repito lo mismo para los valores de V

@callback(Output("rgslider-v-pajama", "value",allow_duplicate=True),
        Input("Vmin", "value"),Input("Vsel", "value"),Input("Vmax", "value"),
        prevent_initial_call=True)
def update_v_slider(min,sel,max):
    """Modifico el slider de V en el pajama plot
     con los valores de los inputs si se modifican"""
    _,V,_ = pgut.dd
    return utpj.update_slider_vals(V,min,sel,max)


@callback(Output("Vmin", "value",allow_duplicate=True),
          Output("Vsel", "value",allow_duplicate=True),
          Output("Vmax", "value",allow_duplicate=True),          
          Input("rgslider-v-pajama", "value"),
          prevent_initial_call=True)
def update_v_inputs(V_rang):
    """Modifico los inputs de V en el pajama plot si se modifica el slider"""
    _,V,_ = pgut.dd
    return utpj.update_v_inputs(V,V_rang)

    
@callback(Output("rgslider-v-pajama", "value",allow_duplicate=True),
          Input("rgslider-V", "value"),
          prevent_initial_call=True)
def update_pajama_V_range(V_rang):
    """modifico el pajama v slider si se modifica el 3d slider de V"""
    return V_rang


@callback(Output("rgslider-V", "value",allow_duplicate=True),
            Input("rgslider-v-pajama", "value"),
            prevent_initial_call=True)
def update_V_range(V_rang):
    """modifico el 3d slider de V si se modifica el pajama v slider"""
    return V_rang



#%% Callbacks de download files


    
@callback(Output("Download","data",allow_duplicate=True),
          Input("btn-dwnld-vcte","n_clicks"),
          State("rgslider-b-pajama", "value"),
          State("rgslider-v-pajama", "value"),
          prevent_initial_call=True,
        )
def download_vtrace_vals(click,B_rang,V_rang):
    data = pgut.dd_data
    output_df,csv_name =utpj.get_cte_trace_df(data,B_rang,V_rang,True)
    return dcc.send_data_frame(output_df.to_csv,csv_name)
    
@callback(Output("Download","data",allow_duplicate=True),
          Input("btn-dwnld-bcte","n_clicks"),
          State("rgslider-b-pajama", "value"),
          State("rgslider-v-pajama", "value"),
          #State("shared-data", "data"),
          prevent_initial_call=True,
        )
def download_vtrace_vals(click,B_rang,V_rang):#,data):
    data = pgut.dd_data
    output_df,csv_name =utpj.get_cte_trace_df(data,B_rang,V_rang,vcte=False)
    return dcc.send_data_frame(output_df.to_csv,csv_name)


@callback(Output("Download","data",allow_duplicate=True),
            Input("btn-dwnld-img","n_clicks"),
            State("rgslider-b-pajama", "value"),
            State("rgslider-v-pajama", "value"),
            #State("shared-data", "data"),
            prevent_initial_call=True,
)
def download_img_vals(click,B_rang,V_rang):#,data):
    data = pgut.dd_data
    output_df,csv_name =utpj.get_img_df(data,B_rang,V_rang)
    return dcc.send_data_frame(output_df.to_csv,csv_name)



#%%



#%%



#----------------------- Old Callbacks -----------------------------
# En esta sección guardo los callbacks originales que estoy reformateando
# para separar y convertir en callbacks más pequeños, la idea es 
# ahorrar la cantidad de datos que van y vuelven al server para ver si 
# aumenta la velocidad



# @callback(Output("rgslider-b-pajama", "value",allow_duplicate=True),
#           Output("rgslider-v-pajama", "value",allow_duplicate=True),
#           Output("Bmin", "value"),
#           Output("Bsel", "value"),
#           Output("Bmax", "value"),
#           Output("Vmin", "value"),
#           Output("Vsel", "value"),
#           Output("Vmax", "value"),
          
#           Input("rgslider-b-pajama", "value"),
#           Input("rgslider-v-pajama", "value"),
#           Input("Bmin", "value"),
#           Input("Bsel", "value"),
#           Input("Bmax", "value"),
#           Input("Vmin", "value"),
#           Input("Vsel", "value"),
#           Input("Vmax", "value"),
          

#           State("shared-data", "data"), #unused?
#           prevent_initial_call=True, )
# def update_pajama_ranges(B_rang,V_rang,
#                           bm,bs,bM,
#                           vm,vs,vM,
#                           data):
#     trigger = ctx.triggered_id
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])

#     if trigger == "rgslider-b-pajama":
#         bm,bs,bM = utpj.update_b_inputs(B,B_rang)
#     if trigger == "rgslider-v-pajama":
#         vm,vs,vM = utpj.update_v_inputs(V,V_rang)
#     if trigger in ["Bmin","Bmax"]:
#         B_rang = update_slider_vals(B,bm,bs,bM,B_rang)
#     if trigger in ["Vmin","Vmax"]:
#         V_rang = update_slider_vals(V,vm,vs,vM,V_rang)
    

#     return B_rang,V_rang,bm,bs,bM,vm,vs,vM
       

