Ext.define('MSCSTAT.view.Header', {//заголовок и глобальноеменю
    extend: 'Ext.Container',
    xtype: 'appHeader',
    height: 65,
    layout: {
        type: 'border',
        align: 'middle'
    },
    bodyBadding: 10,
            defaults:{
                margin:10
            },
    initComponent: function() {
        this.items = [{//логотип приложения
            xtype: 'component',
            region: "west",
            margin: '2 5 2 20',
            html: '<img src="/static/js/sencha/resources/images/logo.png" alt="" width="198" height="60"  class="logogradient">'
        },{//группа кнопок меню
        	xtype: 'buttongroup',
        	region: "center",
        	margin: '2 0 2 20',
        	//autoScroll:true,
        	defaults: {
      			scale: "large",
      			iconAlign: "top",
      			autoWidth: true
    		},
    		items:[{
            		tooltip: 'Пользователи',
            		iconCls: 'icon-users', 
            		action: 'users_view'
            	},{
                    xtype:'button',
                    iconCls: 'icon-notifications',
                    tooltip: 'Сообщения',
                    itemId: 'notifications',
                    action: 'notifications_view',
                    plugins:[
                    {
                        ptype:'badgetext',
                        defaultText: 0,
                        enableBg: 'orange',
                        align:'right',
                        disableBg: 'grey',
                        disableOpacity:.5
                    }]
                }
            ]
        },{
        	xtype: 'buttongroup',
        	region: "east",
        	margin: '2 0 2 2',
        	defaults: {
      			scale: "large",
      			iconAlign: "top",
      			autoWidth: true
    		},
            items:[
                {
    			    xtype: 'button',
                    listeners: {
                        'beforerender': function(button) {
                            extAction.getUserData(function(response){
                                button.setText(response.msg.name)
                            });
                        }
                    }
    			},{
        			iconCls: 'icon-change-password',
        			handler: function() {
            		    window.location = '/accounts/change_password/';//смена пароля - переход по ссылке
        			}
        		},{
        			iconCls: 'icon-exit',
    				handler: function() {
            			window.location = '/accounts/logout/';//выход из системы - переход по ссылке
        			}
    			}]
        	}			
        ],
        this.callParent();
    }
});
