Ext.define('MSCSTAT.view.reports.KpiShow', {
    extend:'Ext.view.View',
    xtype:'appKpiShow',
    itemSelector:'tplInfoShow',
    padding: '10px 10px 10px 10px',
    listeners: {
        viewready: {
            fn: function(){ 
                var my = this;
                var runner = new Ext.util.TaskRunner();
			    var task = runner.start({
				     run: this.StatusUpdate,
				     interval: 360000,
				     args: [my]
				});
            }
        }
    },
    config: {
	    itemTpl: [
	        '<tpl>',
	        '<table border="1" cellpadding="5" style="font-size:10pt;text-align:center;vertical-align:middle" text-align="center">',
	            '<tr>',
	                '<td colspan="1"><b>Филиал</b></td>',
	                '<td colspan="1"><b>Дата</b></td>',
	                '<td colspan="1"><b>Время</b></td>',
	                '<td colspan="1"><b>CSetR</b></td>',
	                '<td colspan="1"><b>SucV</b></td>',
	                '<td colspan="1"><b>mACR</b></td>',
	                '<td colspan="1"><b>Calls</b></td>',
	                '<td rowspan="1"><b>IN fail</b></td>',
	                '<td rowspan="1"><b>IN abort</b></td>',
	            '</tr>',
                '<tpl for="content">',
		            '<tr>',
		                '<td><b>{filial}</b></td>',
		                '<td>{date}</td>',
		                '<td>{time}</td>',
		                '<td>{csetr}</td>',
		                '<td>{sucv}</td>',
		                '<td>{macr}</td>',
		                '<td>{calls}</td>',
                        '<td>{in_fail}</td>',
                        '<td>{in_abort}</td>',
		            '</tr>',
	            '</tpl>',
	        '</table>',
	        '</tpl>'
		]
    },
    StatusUpdate: function(my) {
	    Ext.Ajax.request({
            url: '/status/',
            params: {
                report_type: "kpi_show"
            },
            success: function(response, opts) {
                var data = Ext.decode(response.responseText);
                my.update(data);
            }
        });
	}
});