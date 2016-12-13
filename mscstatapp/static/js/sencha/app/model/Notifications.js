Ext.define('MSCSTAT.model.Notifications', {
    extend: 'Ext.data.Model',
    fields: [
    	'id',
    	'sender',
    	'user',
    	'message',
    	'date',
        {name: 'read', type:'boolean'},
        {name: 'sendsms', type:'boolean'}
   ]
});