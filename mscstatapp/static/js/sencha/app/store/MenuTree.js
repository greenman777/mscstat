Ext.define('MSCSTAT.store.MenuTree', {
    extend: 'Ext.data.TreeStore',
    fields: ['text', 'app','filterapp','typeapp','title'],
    id: 'menutree_store',
    proxy: {
        type: 'rest',
        url: 'menutree',
        reader: {
            type: 'json',
            successProperty: 'success'
        },
    	actionMethods: {
            read: 'GET'
        }
    },
    root: {
        text: 'Tree',
        id: 'src',
        expanded: true
  	}
});