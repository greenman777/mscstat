Ext.define('MSCSTAT.Application', {
    extend: 'Ext.app.Application',
    name: 'MSCSTAT',
    appFolder: 'static/js/sencha/app',
    stores: [
        'Notifications','MenuTree','Mss','Object','TaskComments','TaskHistory','Tasks','Priority','TaskStatus','Users'
    ],
    views: [
        'MSCSTAT.view.notifications.List.Controller',
        'MSCSTAT.view.notifications.Edit.Controller',
        'MSCSTAT.view.notifications.Filter.Controller',
        'MSCSTAT.view.task_comments.ListController',
        'MSCSTAT.view.task_comments.EditController',
        'MSCSTAT.view.users.ListController',
        'MSCSTAT.view.TabPanel',
        'MSCSTAT.view.Header',
        'MSCSTAT.view.MenuPanel',
        'MSCSTAT.view.Tasks',
        'MSCSTAT.view.Users',
        'MSCSTAT.view.Notifications',
        'MSCSTAT.view.reports.AdaptiveReport',
        'MSCSTAT.view.reports.KpiShow'
    ],
    init: function() {
        Ext.getBody().mask("Загрузка приложения...");
        extAction.getUserData(function(response){
            MSCSTAT.global.Vars.user_id = response.msg.id;
            MSCSTAT.global.Vars.user_name = response.msg.name;
        });
    },
    launch: function() {
        Ext.tip.QuickTipManager.init();
        var task = new Ext.util.DelayedTask(function() {
            Ext.getBody().unmask({
                duration: 500,
                remove: true
            });
        });
        task.delay(1000);
    }
});