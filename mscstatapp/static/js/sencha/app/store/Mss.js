Ext.define('MSCSTAT.store.Mss', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.Mss',
    autoLoad:true,
    proxy: {
        type: 'rest',
        url: 'mss',
        reader: {
        	totalProperty: 'count',
            type: 'json',
            successProperty: 'success'
        },
        writer: {
        	writeAllFields: true,
           	encode: false,
            type: 'json'
        }
    }
});