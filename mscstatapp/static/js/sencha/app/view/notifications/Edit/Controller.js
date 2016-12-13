Ext.define('MSCSTAT.view.notifications.Edit.Controller', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.NotificationsEdit',
    
    sendMessages: function(button) {
        var my = this;
        var win = button.up('window');
        var form = win.down('form');
        if (form.isValid()) {
        	Ext.Ajax.request({
	            url: '/send_notification/',
	            params:{
	               message: form.getValues().name,
	               recipients: Ext.JSON.encode(form.getValues().recipients),
	               sendsms: form.getValues().sendsms
	            },
	            success: function(response, opts) {
	                var obj = Ext.decode(response.responseText);
	                var content = obj.messages;
	                Ext.Msg.alert('Извещение', content);
	                
	            }
        	});
            win.close();
        }
    }
});