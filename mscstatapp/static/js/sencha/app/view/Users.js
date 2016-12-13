Ext.define('MSCSTAT.view.Users', {
    extend: "Ext.panel.Panel",//наследуем родительский класс
    xtype:'appUsers',
    layout: {
        type: 'border',
        align: 'stretch',
        padding:5
    }, 
    requires: [//подгружаем классы виджетов
        'MSCSTAT.view.users.List',
        'MSCSTAT.view.users.Details'
    ],
    //инициализируем свойства (конструктор объекта)
    initComponent: function () {
        Ext.apply(this, {
            items: [{
            	region: 'center',
        		xtype: 'appUsersList',
        		flex:3
    		},{
    			region: 'east',
            	collapsible:true,
                split:true,
                title:'Подробности',
                xtype: 'panel',
                itemId:'panelUsersDetails',
                
                autoScroll:true,
                flex:1,
                items: [{
                    xtype: 'appUsersDetails'
                }]
          	}]
        });
        //инициализируем родительский класс;
        this.callParent(arguments);
    }
});