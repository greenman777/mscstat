Ext.define('MSCSTAT.view.notifications.Edit.View', {
    extend: 'Ext.window.Window',
    xtype: 'appNotificationsEdit',
    title: 'Редактирование сообщения',
    controller: 'NotificationsEdit',
    modal : true,
    width:600,
    initComponent: function() {
    	var my = this;
        this.items = [{
        	xtype: 'form',
        	frame: true,
        	defaults: {anchor: '100%',padding: '5 5 5 5'},
            items: [
            {   xtype: 'textfield',name : 'id',hidden:true},
            {  
                xtype: 'textareafield',
                name: 'name',
                fieldLabel: 'Сообщение',
                maxLength: 150,
                allowBlank:false,
                height: 6
            },{
                xtype: 'tagfield',
                fieldLabel: 'Получатели',
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
            },{  
            	xtype: 'checkbox',
                boxLabel: 'Отправить SMS',
                name: 'sendsms',
                checked:'true',
                inputValue: 'true',
                uncheckedValue: 'false'
            }]
        }];
        this.buttons = [{
            iconCls: 'icon-email_send',
        	text: 'Отправить',
            handler: 'sendMessages'
        },{
        	text: 'Отмена',
            handler: function(){
                my.close();
            }
        }];
        this.callParent(arguments);
    }
});