Ext.define('MSCSTAT.view.notifications.Filter.View', {
    extend: 'Ext.window.Window',
    xtype: 'appNotificationsFilter',
    controller: 'NotificationsFilter',
    title: 'Выберите поля для фильтрации',
    width:400,
    layout: 'fit',
    resizable: false,
    closeAction: 'hide',
    modal : true,
    initComponent: function() {
        this.items = [{
        	xtype: 'form',
        	layout: 'anchor',
            bodyStyle: {
                background: 'none',
                padding: '10px',
                border: '0'
            },
            defaults: {
                xtype: 'textfield',
                anchor: '100%'
            },
            items: [
            {
                xtype: 'tagfield',
                fieldLabel: 'Имя отправителя',
                name: 'recipients',
                autoSelect: true,
                queryMode: 'remote',
                labelTpl: "{last_name} {first_name}",
                displayField: 'last_name',
                listConfig: {
                    getInnerTpl: function(){
                        return '{last_name} {first_name}';
                    }
                },
                valueField: 'id',
                store: 'Users'
            }]
        }];
        this.buttons = [{
            iconCls: 'icon-filter',
        	text: 'Применить',
            action: 'filter'
        },{
            text: 'Сбросить',
            handler: function () { this.up('window').down('form').getForm().reset(); }
        },
        {
            text: 'Отмена',
            handler: function () { this.up('window').close(); }
        }];
        this.callParent(arguments);
    }
});