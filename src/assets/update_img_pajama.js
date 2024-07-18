

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside_pajama_img: {
        update_img_pajama: function(rg_b_pajama, rg_v_pajama, data, 
                fig_img) {
            
            if ([data,rg_b_pajama,rg_v_pajama].some(item => item ==null)){
             // data==null|| rg_b_pajama==null || rg_v_pajama==null){
                return fig_img
            }
            const {B,V,r} = data
            const [bs,bsel , be] = rg_b_pajama;
            const [vs,vsel , ve] = rg_v_pajama;

            const b = B.slice(bs, be);
            const v = V.slice(vs, ve);
            //const rs = r.slice(vStart, vEnd).map(row => row.slice(bStart, bEnd));
            const rs = r.slice(vs, ve).map(row => row.slice(bs, be));
            
            const fig_img_new = {...fig_img}; //Object.assign({}, fig_img)
            //toda la imagen            
            fig_img_new['data'][0]['x'] = b;
            fig_img_new['data'][0]['y'] = v;
            fig_img_new['data'][0]['z'] = rs;
            // corte horizontal
            fig_img_new['data'][1]['x'] = [ B[bsel] ,B[bsel] ];
            fig_img_new['data'][1]['y'] = [v[0],v[v.length-1]];
            // corte vertical
            fig_img_new['data'][2]['x'] = [b[0],b[b.length-1]];
            fig_img_new['data'][2]['y'] = [V[vsel],V[vsel]];

            return fig_img_new
        },


    update_pajama_b_trace : function(rg_b_pajama,rg_v_pajama, data, fig_bcte) {
        if (data==null || rg_b_pajama==null){
            return fig_bcte
        }
        const {V,r} = data
        const [bs,bsel , be] = rg_b_pajama;
        const [vs,vsel , ve] = rg_v_pajama;
        vsect = V.slice(vs,ve)
        rsect = r.slice(vs,ve).map(i => i[bsel])
        
        const fig_bcte_new = {...fig_bcte}//Object.assign({}, fig_bcte)
        fig_bcte_new['data'][0]['y'] = vsect
        fig_bcte_new['data'][0]['x'] = rsect

        return fig_bcte_new        
        
    },

    update_pajama_v_trace : function(rg_b_pajama,rg_v_pajama, data, fig_vcte) {
        if (data==null|| rg_v_pajama==null){
            return fig_vcte
        }
        const {B,r} = data
        const [bs,bsel , be] = rg_b_pajama;
        const [vs,vsel , ve] = rg_v_pajama;
        bsect = B.slice(bs,be)
        rsect = r[vsel].slice(bs,be)
        
        const fig_vcte_new = {...fig_vcte}//Object.assign({}, fig_vcte)
        fig_vcte_new['data'][0]['x'] = bsect
        fig_vcte_new['data'][0]['y'] = rsect

        return fig_vcte_new
    },
}
});