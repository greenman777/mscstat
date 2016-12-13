Ext.define('MSCSTAT.view.task_history.List' ,{
    extend: 'Ext.grid.Panel',
    xtype: 'appTaskHistoryList',
    controller: 'TaskHistoryList',
    columnLines: true,
    store : 'TaskHistory',
    title: '<b>История задачи</b>',
    initComponent: function() {
        this.columns = [
  			{  xtype:'rownumberer',width:30},
			{
				header: 'Корректор', 
				flex: 1,
				renderer: function(value, meta, record, rowIndex, colIndex, store, view) {
                    store = Ext.data.StoreManager.lookup('Users');
                    user_rec = store.getById(record.get('corrector'));
                    if (user_rec != null){
                        corrector_fullname = user_rec.get('first_name')+" "+user_rec.get('last_name');
                        meta.tdAttr = 'data-qtip="' + corrector_fullname + '"';
                        return corrector_fullname; 
                    }
                }
			},{
                header: 'Комментарий',
                dataIndex: 'comment',
                flex: 3,
                renderer: function (value, meta, record) {
                    meta.tdAttr = "data-qtip='" + value + "'";
                    return value;
                }
            },{
                header: 'Дата', 
                dataIndex: 'create_date'
            },{
				header: 'Статус', 
				renderer: function(value, meta, record, rowIndex, colIndex, store, view) {
                    store = Ext.data.StoreManager.lookup('TaskStatus');
                    status_rec = store.getById(record.get('status'));
                    if (status_rec != null){
                        status_name = status_rec.get('name');
                        return status_name; 
                    }
                }
			},
			{xtype:'actioncolumn',
        		width:22,
        		handler:'deleteRecord',
        		items: [{
        			iconCls: 'icon-delete',
        			tooltip: 'Удалить'
       			}],
                listeners: {
                    scope:this,
                    'afterrender': function(action){
                        var typeapp = this.up('appTasks').typeapp; 
                        if (typeapp =='tasks_all') {
                            action.hidden = true;
                        }
                    }
                }
       		},
       		{xtype:'actioncolumn',
       			width:22,
       			handler:'editRecord',
       			items: [{
        			iconCls: 'icon-edit',
        			tooltip: 'Редактировать'
        		}],
                listeners: {
                    scope:this,
                    'afterrender': function(action){
                        var typeapp = this.up('appTasks').typeapp; 
                        if (typeapp =='tasks_all') {
                            action.hidden = true;
                        }
                    }
                }
    		}
        ];
        this.dockedItems = [{
            xtype: 'toolbar',
            items: 
	        ['->',{
	            iconCls: 'icon-task_history_add',
	            itemId: 'add',
	            text: 'Добавить запись',
	            handler: 'addRecord',
	            listeners: {
	                scope:this,
	                'afterrender': function(action){
	                    var typeapp = this.up('appTasks').typeapp; 
	                    if (typeapp =='tasks_all') {
	                        action.hidden = true;
	                    }
	                }
	            }
	        },{
	            iconCls: 'icon-update',
	            itemId: 'update',
	            tooltip: 'Обновить',
	            handler: 'updateRecord'
	        }]
        }];
        this.callParent(arguments);
    }
});