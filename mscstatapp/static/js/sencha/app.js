Ext.Loader.setPath('Ext.ux', 'static/js/sencha/ext/packages/ux/classic/src');
Ext.onReady(function() {
    Ext.util.Format.decimalSeparator = '.';
    Ext.require(["Ext.util.Cookies", "Ext.Ajax"], function(){
		// Add csrf token to every ajax request
		var token = Ext.util.Cookies.get('csrftoken');
		Ext.Ajax.setTimeout(300000);
		if(!token){
			Ext.Error.raise("Missing csrftoken cookie");
		} else {
			Ext.Ajax.setDefaultHeaders({
				'X-CSRFToken': token,
				'accept': 'application/json'
			});
		};
    });
});
Ext.application({
	requires: [//подсказываем какие классы загрузить при старте
		'MSCSTAT.global.Vars',
        'Ext.chart.*',
		'Ext.form.action.StandardSubmit',
        'Ext.window.MessageBox',
		'Ext.direct.RemotingProvider',
		'Ext.direct.Manager' ,
		'Ext.data.proxy.Direct'
	],
	name: 'MSCSTAT',//глобальная переменная области видимости приложения
	extend: 'MSCSTAT.Application',
	appFolder: 'static/js/sencha/app',//путь к приложению
	controllers: [//подключаем контроллеры
    	'Interface'
    ],
	autoCreateViewport: true//Viewport создаем автоматичекски
});
