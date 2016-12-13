Ext.define('MSCSTAT.model.Tasks', {
    extend: 'Ext.data.Model',
    fields: [
    	'id',
    	'heading',
    	'description',
    	'author',
    	'performer',
    	'create_date',
    	'execution_date',
    	'priority',
        'status'
   ]
});
