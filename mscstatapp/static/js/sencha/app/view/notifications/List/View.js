Ext.define('MSCSTAT.view.notifications.List.View' ,{
    extend: 'Ext.grid.Panel',
    xtype: 'appNotificationsList',
    controller: 'NotificationsList',
    columnLines: true,
    store : 'Notifications',
    listeners: {
    	selectionchange: 'selectNotifications'
    },
    viewConfig: {
        getRowClass: function (record, rowIndex, rowParams, store) {
            if (! record.get('read')) {
            	if (record.get('sender')==null) {
                    return  'blue-overdue';
                }
                else {
               	   return  'red-overdue';
                }
            }
			else {
                return '';
            }
        },
        listeners: {
            render: function(gridview) {
            	var grid = Ext.getCmp('tabpanel').getActiveTab().down('grid');
            	var store = grid.getStore();
            	store.on('load', function() {	
					var expander = grid.getPlugin('rowexpand');
					store.each(function(record) {  
						if (record.get('read')==false){
							//expander.toggleRow(store.indexOf(record),record);	
						}
					});
				});
            },
            viewready: function(grid) {
                grid.focus();
                new Ext.util.DelayedTask(function(){
					grid.getSelectionModel().select(0);
				}).delay(500);
            }
        }
    },
	/*
    plugins: [{
        ptype: 'rowexpander',
        rowBodyTpl : [
            '<p><b>Сообщение:</b> {message}</p>'
        ],
        pluginId: 'rowexpand'
    }],
	*/
    initComponent: function() {
    	//this.store = Ext.data.StoreManager.lookup('Notifications');
        this.columns = [
      			{   xtype:'rownumberer',width:40},
				{
					header: 'Отправитель',
					flex: 2,
					dataIndex : 'sender_name',
					renderer: function(value, meta, record, rowIndex, colIndex, store, view) {
						store = Ext.data.StoreManager.lookup('Users');
                        sender_rec = store.getById(record.get('sender'));
                        if (sender_rec != null){
                            sender_name = sender_rec.get('first_name')+" "+sender_rec.get('last_name');
                            record.data.sender_name = sender_name;
	                        meta.tdAttr = 'data-qtip="' + sender_name + '"';
	                    }
	                    else {
	                    	sender_name = "Система";	
	                    }
	                    return sender_name;
   					}
				},{
                    header: 'Дата отправки', 
                    flex: 1,
                    dataIndex: 'date',
                    format: 'Y-m-d H:i'
                },{
	                header: 'Сообщение', 
	                dataIndex: 'message',
	                flex: 5,
	                renderer: renderMessage
	            },{
		            header: 'Прочитано',
		            xtype: 'booleancolumn',
		            dataIndex: 'read',
		            trueText:'Да',
		            falseText:'Нет',
		            flex: 1,
		            renderer: function(value,meta,o) {
		                var fontweight = value ? 'normal' : 'bold';
		                value=value? 'Да' : 'Нет';
		                meta.style='font-weight:'+fontweight;
		                return value;
		            }
		        },{
		        	xtype:'actioncolumn',
            		width:22,
            		items: [{
            			iconCls: 'icon-delete',
            			tooltip: 'Удалить',
            			handler:'deleteRecord'
           			}]
           		}
            ];
        this.dockedItems = [{
            xtype: 'toolbar',
            items: [
			{
                iconCls: 'icon-filter_add',
                itemId: 'filter_add',
                tooltip: 'Отфильтровать данные',
                handler: 'addFilter'
            },{
                iconCls: 'icon-filter_delete',
                itemId: 'filter_delete',
                tooltip: 'Сбросить фильтр',
                handler: 'delFilter'
            },
            '->',
			{
	            iconCls: 'icon-message_send',
	            itemId: 'create_message',
	            tooltip: 'Создать сообщение',
	            text: 'Создать сообщение',
	            handler: 'createMessage'
            },{
	            iconCls: 'icon-update',
	            itemId: 'update',
	            tooltip: 'Обновить',
	            handler: 'updateRecord'
            }]
        },{
            xtype: 'pagingtoolbar',
            store: 'Notifications',
            dock: 'bottom',
            displayInfo: true,
            beforePageText: 'Страница',
            afterPageText: 'из {0}',
            displayMsg: 'Сообщения {0} - {1} из {2}',
            listeners: {
                change: 'changePage'
            }
        }];
        this.callParent(arguments);
        function renderMessage(value, p, record) {
	        return Ext.String.format(
	            '<b>{0}</b>',
	            value
	        );
    	}
    }
});