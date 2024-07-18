window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_3d: {
        update_gr: function(data, figure) {


            if (data == null){
                return figure
            }
            /*console.log("called update_3d_graph with data:")
            console.log(data)*/

            
            const wall_pos = data['wall_pos']
            
            let [sx,sel_x,ex] = data['B_rang'] //esta se puede modificar
            let [sy,sel_y,ey] = data['V_rang']

            if (ex == 0){
                ex = data['x'].length - 1;
                }
            if (ey == 0){
                ey = data['y'].length - 1;
                }
                
            const {B:x_data, V:y_data, r:z_data} = data

            
            const x = x_data.slice(sx, ex + 1) //array variation
            const y = y_data.slice(sy, ey + 1)
            const z = z_data.slice(sy, ey + 1).map(i => i.slice(sx, ex + 1))
            
            //surface    
            const fig_data_new = {...figure}

            // fig_data_new['data'][0]['x'] = x
            // fig_data_new['data'][0]['y'] = y
            // fig_data_new['data'][0]['z'] = z
            Object.assign(fig_data_new['data'][0], {x,y,z});
                
            //bcte_on_wall
            const z_bcte_on_wall = z_data.map(i => i[sel_x]).slice(sy,ey)//+1)
            fig_data_new['data'][1]['x']= (new Array(y.length)).fill(wall_pos['x'][0])
            fig_data_new['data'][1]['y']= y
            fig_data_new['data'][1]['z']= z_bcte_on_wall
            //bcte_on_surf
            fig_data_new['data'][2]['x']= (new Array(y.length)).fill(x_data[sel_x])
            fig_data_new['data'][2]['y']= y
            fig_data_new['data'][2]['z']= z_bcte_on_wall
            //bcte_on_floor
            fig_data_new['data'][3]['x']= (new Array(y.length)).fill(x_data[sel_x])
            fig_data_new['data'][3]['y']= y
            fig_data_new['data'][3]['z']= (new Array(y.length)).fill(wall_pos['z'][0])
            
            //vcte_on_wall
            const z_vcte_on_wall = z_data[sel_y].slice(sx,ex)//+1)
            fig_data_new['data'][4]['x'] = x
            fig_data_new['data'][4]['y'] = (new Array(x.length)).fill(wall_pos['y'][0])
            fig_data_new['data'][4]['z'] = z_vcte_on_wall
            //vcte_on_surf
            fig_data_new['data'][5]['x'] = x
            fig_data_new['data'][5]['y'] = (new Array(x.length)).fill(y_data[sel_y])
            fig_data_new['data'][5]['z'] = z_vcte_on_wall
            //vcte_on_floor
            fig_data_new['data'][6]['x'] = x
            fig_data_new['data'][6]['y'] = (new Array(x.length)).fill(y_data[sel_y])
            fig_data_new['data'][6]['z'] = (new Array(x.length)).fill(wall_pos['z'][0])
            
            //img_on_floor
            const z_squeeze = (new Array(y.length)).fill((new Array(x.length)).fill(wall_pos['z'][0]))
            fig_data_new['data'][7]['x'] = x
            fig_data_new['data'][7]['y'] = y
            //z is a matrix like z_data  filled with wall_pos['z'][0]
            fig_data_new['data'][7]['z'] = z_squeeze
            fig_data_new['data'][7]['surfacecolor'] = z

            return fig_data_new




            
        }





    }
});





