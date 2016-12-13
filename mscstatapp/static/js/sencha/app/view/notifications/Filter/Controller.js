Ext.define('MSCSTAT.view.notifications.Filter.Controller', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.NotificationsFilter',

	onAddFilter: function(record) {
		var win = this.getView();
		console.log(record);
        win.show();
	}
});