Ext.define('MSCSTAT.view.MenuPanel', {//древовидное меню приложения
    extend: "Ext.panel.Panel",
    xtype:'appMenuPanel',
    id:'menupanel',
    initComponent: function() {
        Ext.apply(this, {
            xtype:'panel',
            title:'Разделы',
            width: 235,
            split: true,
            collapsible:true,
            autoScroll:true,
            layout: {
                type: 'border',
                align: 'stretch'
            },
            items: [{
            	region: 'center',
                xtype: 'treepanel',
                border: false,
                margin:'5 4 0 4',
                height: '98%',                  
                rootVisible: false,
                store: 'MenuTree'
            }]
        });
        this.callParent(arguments);
    }
});