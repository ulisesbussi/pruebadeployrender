from dash import Input,Output,Patch,State,callback,ctx,no_update
from dash import clientside_callback

from utils import page as pgut


from pages.shared_pajama import shared_pajama

#------------------------Callbacks----------------------------------------


@callback(Output('shared-data', 'data', allow_duplicate=True),
          Input('rgslider-V', 'value'),
          Input('rgslider-B', 'value'),
          prevent_initial_call=True
)
def update_data_slider(V_rang,B_rang):
    data_patch = Patch()
    data_patch['V_rang'] = V_rang
    data_patch['B_rang'] = B_rang
    return data_patch



from dash import ClientsideFunction

clientside_callback(
    ClientsideFunction(
        namespace='clientside_3d',
        function_name='update_gr'
    ),
    Output('3d-graph', 'figure'),
    Input('shared-data', 'data'),
    State('3d-graph', 'figure'),
    prevent_initial_call=True
)




# @callback(Output("3d-graph", "figure"),
          
#           Input("rgslider-V", "value"),
#           Input("rgslider-B", "value"),
          
#           #State("shared-data", "data"),
#           prevent_initial_call=True
# )
# def update_graph(V_rang, B_rang):#, data):


#     B,V,r = pgut.get_BVr2()#pgut.get_BVr(data)

#     fig_range_dic = pgut.get_fig_range_dic(B,V,r) #used to set lines on walls
    

#     patched_fig = Patch()
#     #update surface_plot
#     patched_fig = pgut.update_surf_trace(B,V,r, 
#                                         patched_fig, 
#                                         B_rang,V_rang,
#                                         fig_range_dic)    
#     #update B=cte and V=cte traces
#     patched_fig = pgut.update_Bcte_val(B,V,r, 
#                                        patched_fig,
#                                        B_rang,V_rang,
#                                        fig_range_dic)
#     patched_fig = pgut.update_Vcte_val(B,V,r, 
#                                        patched_fig,
#                                        B_rang,V_rang,
#                                        fig_range_dic)
   
#     patched_fig = pgut.update_squeeze_val(B,V,r,
#                                           patched_fig,
#                                           B_rang,V_rang,
#                                           fig_range_dic)
    
#     return patched_fig




# #here the javascript callback to set 3d-graph range
# clientside_callback(
# """
# function updata_gr(data,figure){
    

#     let wall_pos = data['wall_pos']
#     let sx    = data['B_rang'][0]
#     let ex    = data['B_rang'][2]
#     let sy    = data['V_rang'][0]
#     let ey    = data['V_rang'][2]
#     let sel_x = data['B_rang'][1]
#     let sel_y = data['V_rang'][1]
    
#     if (ex == 0){
#         ex = data['x'].length - 1;
#         }
#     if (ey == 0){
#         ey = data['y'].length - 1;
#         }
#     let x_data = data['B']
#     let y_data = data['V']
#     let z_data = data['r']
    
#     let x = x_data.slice(sx, ex + 1)
#     let y = y_data.slice(sy, ey + 1)
#     let z = z_data.slice(sy, ey + 1).map(i => i.slice(sx, ex + 1))
    
#     //surface    
#     const fig_data_new = Object.assign({}, figure)
#     fig_data_new['data'][0]['x'] = x
#     fig_data_new['data'][0]['y'] = y
#     fig_data_new['data'][0]['z'] = z

#     //bcte_on_wall
#     let y_bcte_on_wall = y_data.slice(sy, ey)// + 1)
#     let z_bcte_on_wall = z_data.map(i => i[sel_x]).slice(sy,ey)//+1)
#     fig_data_new['data'][1]['x']= (new Array(y_bcte_on_wall.length)).fill(wall_pos['x'][0])
#     fig_data_new['data'][1]['y']= y_bcte_on_wall
#     fig_data_new['data'][1]['z']= z_bcte_on_wall
#     //bcte_on_surf
#     fig_data_new['data'][2]['x']= (new Array(y_bcte_on_wall.length)).fill(x_data[sel_x])
#     fig_data_new['data'][2]['y']= y_bcte_on_wall
#     fig_data_new['data'][2]['z']= z_bcte_on_wall
#     //bcte_on_floor
#     fig_data_new['data'][3]['x']= (new Array(y_bcte_on_wall.length)).fill(x_data[sel_x])
#     fig_data_new['data'][3]['y']= y_bcte_on_wall
#     fig_data_new['data'][3]['z']= (new Array(y_bcte_on_wall.length)).fill(wall_pos['z'][0])
    
#     //vcte_on_wall
#     let x_vcte_on_wall = x_data.slice(sx, ex )//+ 1)
#     let z_vcte_on_wall = z_data[sel_y].slice(sx,ex)//+1)
#     fig_data_new['data'][4]['x'] = x_vcte_on_wall
#     fig_data_new['data'][4]['y'] = (new Array(x_vcte_on_wall.length)).fill(wall_pos['y'][0])
#     fig_data_new['data'][4]['z'] = z_vcte_on_wall
#     //vcte_on_surf
#     fig_data_new['data'][5]['x'] = x_vcte_on_wall
#     fig_data_new['data'][5]['y'] = (new Array(x_vcte_on_wall.length)).fill(y_data[sel_y])
#     fig_data_new['data'][5]['z'] = z_vcte_on_wall
#     //vcte_on_floor
#     fig_data_new['data'][6]['x'] = x_vcte_on_wall
#     fig_data_new['data'][6]['y'] = (new Array(x_vcte_on_wall.length)).fill(y_data[sel_y])
#     fig_data_new['data'][6]['z'] = (new Array(x_vcte_on_wall.length)).fill(wall_pos['z'][0])
    
#     //pending squeeze, checkear bug? se corre el bcte solo?
#     return fig_data_new
#     }""", 
#     Output('3d-graph', 'figure'),
    
#     Input('shared-data', 'data'),
#     State('3d-graph', 'figure'),
#     prevent_initial_call=True
# )
