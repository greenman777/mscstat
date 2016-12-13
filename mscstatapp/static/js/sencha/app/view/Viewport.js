Ext.define('MSCSTAT.view.Viewport', {//создаем первичный контейнер Viewport, занимающий все окно браузера
    extend: 'Ext.container.Viewport',//наследуем родительский класс
    layout: 'border',//тип слоя border (делит страницу на пять областей center, north, south, west, east) 
    requires: [//подгружаем классы виджетов
        
    ],
    //инициализируем свойства (конструктор объекта)
    initComponent: function () {
        Ext.apply(this, {
            items: [{//заголовок
        		region: 'north',
        		xtype: 'appHeader'
    		},{//меню приложения
            	region: 'west',
        		xtype: 'appMenuPanel'
          	},{//панель вкладок для таблиц
            	region: 'center',
                xtype: 'appTabPanel'
            }]
        });
        //инициализируем родительский класс;
        this.callParent(arguments);
    }
});