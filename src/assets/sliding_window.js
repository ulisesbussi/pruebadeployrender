window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_sliding_window: {

        update_graphs: function(upd,fourier_data,slicing_data,x_cte_data,shared_data,fig,freqfig) {            
            /*update figures returns [fig, figfreq] */

            let new_fig     = {...fig}
            let new_freqfig = {...freqfig}

            let {pos_idx,window_size_idx,const_val_idx,xmin,xmax} = slicing_data

            if (upd==1) {

                window_x_start = pos_idx + xmin
                window_x_end   = window_x_start + window_size_idx
                if (window_x_end > xmax){  //la ventana termina despues de xmax, no actualizo
                    return [new_fig,new_freqfig]
                }

                if (fourier_data[pos_idx]) {//no freq data exit
                    freq = fourier_data[pos_idx]['freq']
                } else {
                    return [new_fig,new_freqfig]
                }

                let xname = x_cte_data['xname']
                let r     = shared_data['r']
                
                let x_slice = shared_data[x_cte_data['xname']].slice(xmin,xmax)
                
                if (xname == 'B') {    
                    y_slice = r[const_val_idx].slice(xmin,xmax)
                } else if (xname == 'V') {
                    y_slice = r.slice(xmin,xmax).map(i => i[const_val_idx])
                }
                
                new_fig.layout.shapes[0]['x0'] = x_cte_data['x'][window_x_start]
                new_fig.layout.shapes[0]['x1'] = x_cte_data['x'][window_x_end]

                new_fig['data'][0]['x'] = x_slice
                new_fig['data'][0]['y'] = y_slice

                new_freqfig.data[0]['x'] = freq
                new_freqfig.data[0]['y'] = fourier_data[pos_idx]['amplitude']
                new_freqfig.data[1]['x'] = freq
                new_freqfig.data[1]['y'] = fourier_data[pos_idx]['phase']
            }

            return  [new_fig, new_freqfig]
        },


        stop_button: function(click_stop,slicing_data,click_play){
            /*Stops updating returns play_btn_clicks, play_btn_symbol, 
            slicing_data reseting pos, and update-graph elem*/
            // console.log('click_stop',click_stop)
            let new_slicing_data = {...slicing_data}
            if (click_stop==0){// not clicked
                return [click_play,'fa fa-pause mr1',slicing_data,0]
            }
            else {

                new_slicing_data['pos_idx'] = 0 
                new_slicing_data['play'] = false

                return [0,'fa fa-play mr1',new_slicing_data,1]
            }
        },

        play_button:   function(n_clicks,slicing_data){
            /* play action, returns btn_play_symbol, updated slicing-data,
            and changes interval to 24h if not playing*/
            if (n_clicks%2){
                slicing_data['play'] = true
                return ['fa fa-pause mr1',slicing_data,50]
            }else{
                slicing_data['play'] = false
                return ['fa fa-play mr1',slicing_data,60*60*24*1000]
            }
        },


        update_figs_play: function(n_intervals,slicing_data){
            /*update figs on interval if play is true,
            returns update-graph, new slicing-data and btn_stop_clicks */
            
            let {pos_idx,play,stepsize,window_size_idx,xmin,xmax} = slicing_data
            
            pos_idx = pos_idx + stepsize //new pos
            x_start = pos_idx + xmin    //new x_start
            x_end   = x_start + window_size_idx //new x_end

            if (x_end > xmax){
                return [1,slicing_data,1]
            }               
            if (play){    
                slicing_data['pos_idx']  = pos_idx
            }
            return [1,slicing_data,0]
        },



    update_position_btns: function(fsb,sb,sf,fst,slicing_data){
        /*actualiza el resto de los botones, fsb= fast step back, sb= step back,
        sf= step forward, fst= fast step forward. saltando 5 y 10 del stepsize*/
        let {stepsize,pos_idx,xmin,xmax,window_size_idx,n_points} = slicing_data
        let new_slicing_data = {...slicing_data}
        
        let trigger = window.dash_clientside.callback_context.triggered[0]['prop_id']
        let json_trigger = JSON.parse(trigger.split('.')[0])['id']

        steps = {
            'btn-faststepback':-10, 
            'btn-stepback':-5, 
            'btn-stepforward':5, 
            'btn-faststepforward':10
        }
        
        //calculo la nueva posicion np
        let x_start  = pos_idx + xmin
        let np       = x_start + steps[json_trigger]*stepsize
        let np_end   = np + window_size_idx

        //checkeo limites
        if (np <= xmin){
            np = xmin
        }else if (np > xmax){
            np = xmax - window_size_idx
        }

        new_slicing_data['pos_idx'] = np 
        return [new_slicing_data,1]
    },

    }
});