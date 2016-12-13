Ext.define('MSCSTAT.view.Tasks', {
    extend: "Ext.panel.Panel",//наследуем родительский класс
    xtype:'appTasks',
    layout: 'border',
    requires: [//подгружаем классы виджетов
        'MSCSTAT.view.tasks.List',
        'MSCSTAT.view.task_history.List',
        'MSCSTAT.view.task_comments.List'
    ],
    //инициализируем свойства (конструктор объекта)
    initComponent: function () {
        this.compet = true;
        Ext.apply(this, {
            items: [{
                region: 'center',
        		xtype: 'appTasksList',
        		flex:3
    		},{
                region: 'south',
        		xtype: 'panel',
        		flex:2,
        		split: true,
                collapsible:true,
                layout: {
                    type: 'border',
                    align: 'stretch'
                },
                items: [{
                	region: 'center',
	                xtype: 'appTaskHistoryList',
                    flex:3
	            },{
	            	region: 'east',
	            	collapsible:true,
	                split:true,
	                flex:2,
	                title:'Комментарии',
	                xtype: 'appTaskCommentsList'
	            }]
          	}]
        });
        //инициализируем родительский класс;
        this.callParent(arguments);
    }
});