
from dash import (
    Input,Output,State,callback,
    ALL,ctx,no_update, Patch, no_update

)

import numpy as np
import utils_pajama as utpj


#No puedo separar en 2 callbacks porque me arroja circular dependencies error

def update_b_inputs(B,B_rang):
    #change bm and bM
    bm = f"{B[B_rang[2]]:.2f}" 
    bM = f"{B[B_rang[0]]:.2f}" 
    return bm,bM

def update_v_inputs(V,V_rang):
    #change vm and vM
    vm = f"{V[V_rang[0]]:.2f}" 
    vM = f"{V[V_rang[2]]:.2f}" 
    return vm,vM

def update_b_slider(B,bm,bM,B_rang):
    #change B_rang finding nearest indices
    bM = utpj.tryfloat(bM)
    bm = utpj.tryfloat(bm)
    
    if bM is None or bm is None:
        return no_update
    if bM<=bm:
        return no_update
    
    ibM = np.argmin(np.abs(B-bM)) #index of bMax goes to B_rang[0]
    ibm = np.argmin(np.abs(B-bm))
    
    if ibM >= ibm:
        return no_update
    #check if B_rang[1] is in limits if no replace for nearest
    B_rang[0] = ibM
    B_rang[2] = ibm
    if ibM > B_rang[1]:
        B_rang[1] = ibM
    if ibm < B_rang[1]:
        B_rang[1] = ibm
    return B_rang

def update_v_slider(V,vm,vM,V_rang):    
#change V_rang finding nearest indices
    vM = utpj.tryfloat(vM)
    vm = utpj.tryfloat(vm)
    #print(f"vm:{vm}, vM:{vM}")
    #print("updating slider")
    if vM is None or vm is None:
        return no_update
    if vM<=vm:
        #print(f"vM:{vM}, vm:{vm}, vM<=vm")
        return no_update
    #print("vm and vM are ok")
    ivM = np.argmin(np.abs(V-vM))
    ivm = np.argmin(np.abs(V-vm))
    #print(f"indices min:{ivm}, Max:{ivM}")
    if ivm <= ivM:
        return no_update
    #check if V_rang[1] is in limits if no replace for nearest
    V_rang[0] = ivM
    V_rang[2] = ivm
    if ivM > V_rang[1]:
        V_rang[1] = ivM
    if ivm < V_rang[1]:
        V_rang[1] = ivm
    
    return V_rang



# def update_v_slider(V,vm,vM,V_rang):    
# #change V_rang finding nearest indices
#     vM = utpj.tryfloat(vM)
#     vm = utpj.tryfloat(vm)
    
#     if not (vM is None or vm is None):
#         if vM<=vm:
#             return V_rang
#         ivM = np.argmin(np.abs(V-vM))
#         ivm = np.argmin(np.abs(V-vm))
#         #check if V_rang[1] is in limits if no replace for nearest
#         V_rang[0] = ivm
#         V_rang[2] = ivM
#         if ivM < V_rang[1]:
#             V_rang[1] = ivM
#         if ivm > V_rang[1]:
#             V_rang[1] = ivm
#     return V_rang
    
    
@callback(Output("rgslider-b-pajama-3dplot", "value"),
           Output("vcte-pajama-3dplot", "figure"),
           Output("Bmin-3dplot", "value"),
           Output("Bmax-3dplot", "value"),
           Output("Vmin-3dplot", "value"),
           Output("Vmax-3dplot", "value"),
           Output("img-graph-3dplot", "figure"),
           Output("bcte-pajama-3dplot", "figure"),
           Output("rgslider-v-pajama-3dplot", "value"),
          [Input("rgslider-b-pajama-3dplot", "value"),
           Input("rgslider-v-pajama-3dplot", "value"),
           Input("Bmin-3dplot", "value"),
           Input("Bmax-3dplot", "value"),
           Input("Vmin-3dplot", "value"),
           Input("Vmax-3dplot", "value"),],
           State("shared-data", "data"),
           prevent_initial_call=True,
          )
def update_pajama(B_rang,V_rang,bm,bM,vm,vM,data):
    event = ctx.triggered_id
  
    B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
    
    #print(f"V[0]:{V[0]}, V[-1]:{V[-1]}")
    
    if event == "rgslider-b-pajama-3dplot":
        bm,bM = update_b_inputs(B,B_rang)
    if event == "rgslider-v-pajama-3dplot":
        vm,vM = update_v_inputs(V,V_rang)
    
    if event in ["Bmin-3dplot","Bmax-3dplot"]:
        B_rang = update_b_slider(B,bm,bM,B_rang)
    if event in ["Vmin-3dplot","Vmax-3dplot"]:
        #print(f"vm:{vm}, vM:{vM}")
        #print(V_rang)
        V_rang = update_v_slider(V,vm,vM,V_rang)
        
    if B_rang == no_update or V_rang == no_update:
        #print("no update")
        #print(V_rang)
        return no_update,no_update,no_update,\
                no_update,no_update,no_update,\
                no_update,no_update,no_update    
    #update figs
    bcte_dic = utpj.update_Bcte_val(B,V,r,B_rang,V_rang)
    vcte_dic = utpj.update_Vcte_val(B,V,r,B_rang,V_rang)
    img_dic  = utpj.update_img_val(B,V,r,B_rang,V_rang)
    patched_bcte = Patch()
    patched_vcte = Patch()
    patched_img  = Patch()
    patched_bcte = utpj.update_Bcte_trace(patched_bcte,bcte_dic)
    patched_vcte = utpj.update_Vcte_trace(patched_vcte,vcte_dic)
    patched_img  = utpj.update_img_trace(patched_img,img_dic)
    
    return B_rang, patched_vcte, bm, bM, \
            vm, vM, patched_img, patched_bcte, V_rang
   
   
            
#%%            
#%%



# @callback(Output("rgslider-b-pajama-3dplot", "value"),
#            Output("vcte-pajama-3dplot", "figure"),
#            Output("Bmin-3dplot", "value"),
#            Output("Bmax-3dplot", "value"),
#            Output("Vmin-3dplot", "value"),
#            Output("Vmax-3dplot", "value"),
#            Output("img-graph-3dplot", "figure"),
#            Output("bcte-pajama-3dplot", "figure"),
#            Output("rgslider-v-pajama-3dplot", "value"),
#           [Input("rgslider-b-pajama-3dplot", "value"),
#            Input("rgslider-v-pajama-3dplot", "value"),
#            Input("Bmin-3dplot", "value"),
#            Input("Bmax-3dplot", "value"),
#            Input("Vmin-3dplot", "value"),
#            Input("Vmax-3dplot", "value"),],
#            State("shared-data", "data"),
#            prevent_initial_call=True,
#           )
# def update_pajama(B_rang,V_rang,bm,bM,vm,vM,data):
#     event = ctx.triggered_id
#     # print(event)
#     # if event is None:
#     #     return no_update,no_update,no_update,\
#     #             no_update,no_update,no_update,\
#     #             no_update,no_update,no_update
    
        
#     B,V,r = np.array(data['B']),np.array(data['V']),np.array(data['r'])
#     if event == "rgslider-b-pajama-3dplot":
#         #change bm and bM
#         bM = f"{B[B_rang[0]]:.2f}" #aca el 0 es el max
#         bm = f"{B[B_rang[2]]:.2f}" #aca el 2 es el min
#     if event == "rgslider-v-pajama-3dplot":
#         #change vm and vM
#         vm = f"{V[V_rang[0]]:.2f}" #aca el 0 es el min
#         vM = f"{V[V_rang[2]]:.2f}" #aca el 2 es el max
    
#     if event in ["Bmin-3dplot","Bmax-3dplot"]:
#         #change B_rang finding nearest indices
#         bM = utpj.tryfloat(bM)
#         bm = utpj.tryfloat(bm)
#         if not (bM is None or bm is None):
#             ibM = np.argmin(np.abs(B-bM))
#             ibm = np.argmin(np.abs(B-bm))
#             #check if B_rang[1] is in limits if no replace for nearest
#             B_rang[0] = ibM
#             B_rang[2] = ibm
#             if ibM < B_rang[1]:
#                 B_rang[1] = ibM
#             if ibm > B_rang[1]:
#                 B_rang[1] = ibm
#     if event in ["Vmin-3dplot","Vmax-3dplot"]:
#         #change V_rang finding nearest indices
#         vM = utpj.tryfloat(vM)
#         vm = utpj.tryfloat(vm)
#         if not (vM is None or vm is None):
#             ivM = np.argmin(np.abs(V-vM))
#             ivm = np.argmin(np.abs(V-vm))
#             #check if V_rang[1] is in limits if no replace for nearest
#             V_rang[0] = ivm
#             V_rang[2] = ivM
#             if ivM < V_rang[1]:
#                 V_rang[1] = ivM
#             if ivm > V_rang[1]:
#                 V_rang[1] = ivm
        
#     #update figs
#     bcte_dic = utpj.update_Bcte_val(B,V,r,B_rang,V_rang)
#     vcte_dic = utpj.update_Vcte_val(B,V,r,B_rang,V_rang)
#     img_dic  = utpj.update_img_val(B,V,r,B_rang,V_rang)
#     patched_bcte = Patch()
#     patched_vcte = Patch()
#     patched_img  = Patch()
#     patched_bcte = utpj.update_Bcte_trace(patched_bcte,bcte_dic)
#     patched_vcte = utpj.update_Vcte_trace(patched_vcte,vcte_dic)
#     patched_img  = utpj.update_img_trace(patched_img,img_dic)
    
#     print(B_rang)
#     return B_rang, patched_vcte, bm, bM, \
#             vm, vM, patched_img, patched_bcte, V_rang