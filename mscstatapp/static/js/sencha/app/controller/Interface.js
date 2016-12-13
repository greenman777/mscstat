Ext.define('MSCSTAT.controller.Interface', {
    extend: 'Ext.app.Controller',
 	views: ['Header','MenuPanel'],
 	refs: [
 		{ ref: 'appHeader',selector: 'appHeader' },
        { ref: 'appMenuPanel',selector: 'appMenuPanel' },
        { ref: 'appTabPanel',selector: 'appTabPanel' }
    ], 
    init: function() {
        this.control({
        	//'appHeader':{
            //    beforerender: this.startTaskNotifications
            //},
        	'appMenuPanel treepanel': {
        		selectionchange: this.addTabPanel        	        	
        	},
            'appTabPanel': {
            	render: this.KpiAllShow,
                tabchange: this.activTabPanel
            },
            'appHeader button[action=users_view]': {
            	click: {
            		fn: this.viewTopMenu,
            		params: {
            			tab_id:'users_view',app:'appUsers',title:'Список пользователей'	
            		}
            	}
            	
            },
            'appHeader button[action=notifications_view]': {
            	click: {
            		fn: this.viewTopMenu,
            		params: {
            			tab_id:'notifications_view',app:'appNotifications',title:'Уведомления'
            		}
            	}
            }
        });
    },
    
    addTabPanel: function(view, rec, opts) {
        if (rec[0] && rec[0].data.children==null) {  // на всякий случай проверка наличия выделения
            var data=rec[0].data;
        	var tabpanel = this.getAppTabPanel();
            var filterapp = Ext.JSON.decode(data.filterapp);
            var hide_items = Ext.JSON.decode(data.hide_items);
            var tab_id = data.app+data.typeapp;
        	var tab = tabpanel.getComponent(tab_id); // поиск закладки с itemId = data.id
            //снимаем выделение с элемента дерева
            view.deselect(rec);
        	if (tab) {
                 tab.show();
                 tab.focus();
             	 return;
             } // если закладка  существует, она открывается
             tabpanel.add({ // добавляем закладку
             	xtype: data.app,
             	id:tab_id,
                itemId:tab_id,
                typeapp:data.typeapp,
                hide_items:hide_items,
                title:data.title,
                iconCls: 'tabs',
                closable: true
             }).show();
             try {
                tabpanel.setActiveTab(tab_id);
                var grid = tabpanel.getActiveTab().down('grid');
                var store = grid.getStore();
             }
             catch (e) {
                return;
             }
             store.getProxy().extraParams = filterapp;
    		 store.load({
    		 	scope: this,
    			callback: function(records, operation, success) {
        			if (success) {
        				if (records.length > 0){
	        				new Ext.util.DelayedTask(function(){
	    						grid.getSelectionModel().select(0);
							}).delay(1000);
						}
        			}
    			}
			});
        }
	},
	viewTopMenu: function(button, event, eOpts) {
		var params = eOpts.params;
        var tabpanel = this.getAppTabPanel();
        
		var tab = tabpanel.getComponent(params.tab_id); // поиск закладки с itemId
        if (tab) {
             tab.show();
             tab.focus();
             return;
         } // если закладка  существует, она открывается
         tabpanel.add({ // добавляем закладку
            xtype: params.app,
            itemId:params.tab_id,
            title:params.title,
            iconCls: 'tabs',
            closable: true
         }).show();
         tabpanel.setActiveTab(params.tab_id);
         var grid = tabpanel.getActiveTab().down('grid');
         var store = grid.getStore();
         store.getProxy().extraParams = {};
         store.load({
            scope: this,
            callback: function(records, operation, success) {
                if (success) {
                    if (records.length > 0){
	                    new Ext.util.DelayedTask(function(){
							grid.getSelectionModel().select(0);
							grid.focus();
						}).delay(1000);
					};
                }
                return;
            }
        });
	},
    activTabPanel: function(tabPanel, newCard, oldCard, eOpts) {
        try {
		    var grid = newCard.down('grid');
		    var selection = grid.getSelectionModel().getSelection();
        }
		catch (e) {
		  return;
        }
        if (selection.length > 0) {
            grid.getSelectionModel().deselect(selection[0]);
            grid.getSelectionModel().select(selection[0]);
        }
    },
    KpiAllShow: function(tabp) {
        
        var tabpanel = tabp;
        var itemId = 'KpiAllShow';
        var tab = tabpanel.getComponent(itemId); // поиск закладки с itemId = data.id
        if (tab) {
            tab.show();
            tab.focus();
            return;
        } // если закладка  существует, она открывается
        
        tabpanel.add({ // добавляем закладку
           xtype: 'appKpiShow',
           itemId: itemId,
           title:'KPI',
           iconCls: 'tabs',
           closable: true
        }).show();
    },
    taskNotifications: function () {
        var info = Ext.ComponentQuery.query('#notifications')[0];
        Ext.Ajax.request({
		    url: '/notifications_news/',
	        success: function(response, opts) {
		 	    
		 	    var obj = Ext.decode(response.responseText);
	            var count_news = obj.messages['count_news'];
                
                if (count_news == 0) {
	                info.setText("Новых сообщений нет");
	            }
	            else {
	                info.setText("Новых собщений: <b>"+count_news.toString()); 
	                Ext.data.StoreManager.lookup('Notifications').reload();
	            };
		    }
	    });
 	},
    startTaskNotifications: function(view, eOpts) {
        var runner = new Ext.util.TaskRunner();
	    var task = runner.start({
		     run: this.taskNotifications,
		     interval: 120000
		     //args: [view]
		});
    }
});