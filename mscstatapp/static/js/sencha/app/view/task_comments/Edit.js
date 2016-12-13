Ext.define('MSCSTAT.view.task_comments.Edit', {
    extend: 'Ext.window.Window',
    xtype: 'appTaskCommentsEdit',
    controller: 'TaskCommentsEdit',
    title: 'Редактирование комментария',
    modal : true,
    width:400,
    initComponent: function() {
    	my = this;
        this.items = [{
        	xtype: 'form',
        	frame: true,
        	defaults: {anchor: '100%',padding: '5 5 5 5'},
            items: [
            {   xtype: 'combobox',name : 'id',hidden:true},
            {   xtype: 'combobox',name : 'task',hidden:true},
            {   xtype: 'combobox',name : 'author',hidden:true},
			{   xtype: 'datefield',name : 'create_date',format: 'Y-m-d',hidden:true},
            {
                xtype: 'textareafield',
                name : 'comment',
                fieldLabel: 'Комментарий',
                allowBlank:false
            }]
        }];
        this.buttons = [{
            iconCls: 'icon-save',
        	text: 'Сохранить',
            handler: 'saveRecord'
        },{
        	text: 'Отмена',
        	handler: function(){
                my.close();
            }
        }];
        this.callParent(arguments);
    }
});