Ext.define('MSCSTAT.view.task_history.Edit', {
    extend: 'Ext.window.Window',
    xtype: 'appTaskHistoryEdit',
    controller: 'TaskHistoryEdit',
    title: 'Редактирование истории задачи',
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
            {   xtype: 'combobox',name : 'corrector',hidden:true},
			{   xtype: 'datefield',name : 'create_date',format: 'Y-m-d',hidden:true},
            {
                xtype: 'textareafield',
                name : 'comment',
                fieldLabel: 'Комментарий',
                allowBlank:false
            },{
                itemId: 'task_history_status',
                xtype: 'combobox',
                name : 'status',
                fieldLabel: 'Статус',
                queryMode: 'remote',
                editable: false,
                forceSelection:true,
                displayField: 'name',
                valueField: 'id',
                allowBlank:false,
                store: 'TaskStatus'
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
    },
    
    show: function(component, eOpts) {
        //фильтруем доступные статусы
        this.callParent(arguments);
        combo_status = this.down('form').getComponent('task_history_status');
        store_status = combo_status.getStore();
        store_status.clearFilter(true);
        
        typeapp = Ext.getCmp('tabpanel').getActiveTab().typeapp;
        if (typeapp =='tasks_make') {
            store_status.filter('name','на проверку');        
        }
        else if (typeapp =='tasks_check') {
            store_status.filter(function(r) {
                var value = r.get('name');
                return (value == 'выполнена' || value == 'отклонена');
            });
        }
    }
});