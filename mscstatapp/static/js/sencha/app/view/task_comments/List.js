Ext.define('MSCSTAT.view.task_comments.List' ,{
    extend: 'Ext.grid.Panel',
    xtype: 'appTaskCommentsList',
    controller: 'TaskCommentsList',
    columnLines: true,
    store : 'TaskComments',
    title: '<b>Комментарии</b>',
    requires: [//подгружаем классы виджетов
        'MSCSTAT.view.task_comments.Edit'
    ],
    initComponent: function() {
        this.columns = [
  			{  xtype:'rownumberer',width:30},
			{
				header: 'Автор', 
				flex: 1,
				renderer: function(value, meta, record, rowIndex, colIndex, store, view) {
                    var store = Ext.data.StoreManager.lookup('Users');
                    var user_rec = store.getById(record.get('author'));
                    if (user_rec != null){
                        author_fullname = user_rec.get('first_name')+" "+user_rec.get('last_name');
                        meta.tdAttr = 'data-qtip="' + author_fullname + '"';
                        return author_fullname; 
                    }
                }
			},{
                header: 'Комментарий',
                dataIndex: 'comment',
                flex: 3,
                renderer: function (value, meta, record) {
                    meta.tdAttr = 'data-qtip="' + value + '"';
                    return value;
                }
            },{
                header: 'Дата', 
                dataIndex: 'create_date'
            },{xtype:'actioncolumn',
        		width:22,
        		items: [{
        			iconCls: 'icon-delete',
        			tooltip: 'Удалить',
        			handler: 'deleteRecord'
       			}]
       		},
       		{xtype:'actioncolumn',
       			width:22,
       			items: [{
        			iconCls: 'icon-edit',
        			tooltip: 'Редактировать',
        			handler: 'editRecord'
        		}]
    		}
        ];
        
        this.dockedItems = [{
            xtype: 'toolbar',
            items: 
            ['->',{
	            iconCls: 'icon-comments_add',
	            itemId: 'add',
	            text: 'Добавить комментарий',
	            handler: 'addRecord'
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