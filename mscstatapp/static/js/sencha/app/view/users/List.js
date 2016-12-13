Ext.define('MSCSTAT.view.users.List' ,{
    extend: 'Ext.grid.Panel',
    xtype: 'appUsersList',
    columnLines: true,
    header: false,
    controller: 'UsersList',
    store: 'Users',
    listeners: {
    	selectionchange: 'selectUser'
    },
    initComponent: function() {
        this.columns = [
      			{   xtype:'rownumberer',width:30},
				{
				    header: 'Фамилия', 
					flex: 1,
					dataIndex: 'last_name'
				},{
                    header: 'Имя', 
                    flex: 1,
                    dataIndex: 'first_name'
                },{
                    header: 'Дата рождения', 
                    flex: 1,
                    dataIndex: 'birthday'
                },{
                    header: 'E-mail', 
                    flex: 1,
                    dataIndex: 'email',
                    renderer: function (value, meta, record) {
                        meta.tdAttr = "data-qtip='" + value + "'";
                        return value;
                    }
                },{
                    header: 'Телефон', 
                    flex: 1,
                    dataIndex: 'phone'
                },{
                    header: 'Телефон доп.', 
                    flex: 1,
                    dataIndex: 'phone_other'
                },{
                    header: 'Внутр. номер', 
                    flex: 1,
                    dataIndex: 'phone_short'
                },{
                    header: 'Организация', 
                    flex: 1,
                    dataIndex: 'organization_name',
                    renderer: function (value, meta, record) {
                        meta.tdAttr = "data-qtip='" + value + "'";
                        return value;
                    }
                },{
                    header: 'Должность', 
                    flex: 1,
                    dataIndex: 'position',
                    renderer: function (value, meta, record) {
                        meta.tdAttr = "data-qtip='" + value + "'";
                        return value;
                    }
                }
            ];
        this.dockedItems = [{
        	xtype: 'toolbar',
            items:
	        ['->',{
	            iconCls: 'icon-task_add',
	            itemId: 'task_add',
	            text: 'Дать задание',
	            handler: 'addRecord'
	        },{
	            iconCls: 'icon-update',
	            itemId: 'update',
	            tooltip: 'Обновить',
	            handler: 'updateRecord'
	        }]
        },{
            xtype: 'pagingtoolbar',
            store: 'Users',
            dock: 'bottom',
            displayInfo: true,
            beforePageText: 'Страница',
            afterPageText: 'из {0}',
            displayMsg: 'Пользователи {0} - {1} из {2}',
            listeners: {
                change: 'changePage'
            }
        }];
        this.callParent(arguments);
    }
})
