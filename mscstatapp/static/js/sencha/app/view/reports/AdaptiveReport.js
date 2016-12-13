Ext.define('MSCSTAT.view.reports.AdaptiveReport', {
    extend:'Ext.Panel',
    xtype:'appAdaptiveReport',
    layout: 'border',
    listeners: {
        afterrender: {
            fn: function(){ 
            	for(var i=0;i<this.hide_items.length;i++){
            		this.down(this.hide_items[i]).setVisible(false);	
            	}
            }
        }
    },
    initComponent: function() {
    	var my = this;
        Ext.apply(this, {
            items: [{
                region: 'north',
                xtype: 'form',
	            frame: true,
	            reference: 'requestForm',
	            defaults: {anchor: '100%',padding: '5 5 5 5'},
	            items: [{
                    xtype: 'fieldcontainer',
                    layout: 'hbox',
                    defaultType: 'textfield',
                    items:[
                    {
                        xtype: 'combobox',
                        fieldLabel: 'Филиал',
                        name: 'mss',
						labelWidth: 70,
                        allowBlank:false,
                        autoSelect: true,
                        queryMode: 'remote',
                        editable: false,
                        displayField: 'title',
                        margin: '0 10 0 0',
                        valueField: 'id',
                        store: 'Mss',
                        listeners: {
	                        'select': function(combo){
	                        	combo.up('form').down('#objects').setDisabled(false);
                                combo.up('form').down('#objects').clearValue();
	                    	}
	                    }
                    },{
                        xtype: 'tagfield',
                        itemId: 'objects',
                        flex: 1,
                        disabled: true,
                        fieldLabel: 'Объекты',
                        name: 'objects',
                        labelWidth: 70,
                        autoSelect: true,
                        queryMode: 'local',
                        displayField: 'name',
                        margin: '0 10 0 0',
                        valueField: 'id',
                        store: 'Object',
                        listeners: {
	                        'expand': function(combo){
                                var store = combo.getStore();
                                //if (store.getCount()<=0){
                                var typeapp = combo.up('tabpanel').getActiveTab().typeapp;
                                var mss = combo.up('form').getValues().mss;
                                store.load({ params: {mss:mss,typeapp: typeapp}});
                                //};
	                        }
	                    },
                        listConfig: {
                            getInnerTpl: function(displayField) {
                                var typeapp = this.up('tabpanel').getActiveTab().typeapp;
                                if (typeapp == 'mss_intermscho') {
                                    return '{[parseInt(values.name.substring(10, 14),16)]}';
                                }
                                else {
                                    return '{' + displayField + '}';
                                }
                            }
                        }
                    }]
                },{
                    xtype: 'fieldcontainer',
                    layout: 'hbox',
                    defaultType: 'textfield',
                    items:[
                    {
                        xtype: 'datefield',
                        labelWidth: 70,
                        allowBlank:false,
                        name: 'date_start',
                        format: 'Y-m-d',
                        margin: '0 10 0 0',
                        fieldLabel: 'С',
                        value: Ext.Date.add(new Date(), Ext.Date.DAY, -1)
                    },{
                        xtype: 'combobox',
                        itemId: 'hours_start',
                        name : 'hours_start',
                        allowBlank:false,
                        autoSelect: true,
                        editable: false,
                        labelWidth: 15,
                        width: 70,
                        value: "00",
                        fieldLabel: 'ч.',
                        margin: '0 10 0 0',
                        store:["00","01","02","03","04","05","06","07","08","09","10","11",
                               "12","13","14","15","16","17","18","19","20","21","22","23"]
                    },{
                        xtype: 'combobox',
                        itemId: 'c',
                        name : 'minutes_start',
                        labelWidth: 30,
                        allowBlank:false,
                        width: 85,
                        value: "00",
                        autoSelect: true,
                        editable: false,
                        fieldLabel: 'мин.',
                        margin: '0 40 0 0',
                        store:["00","15","30","45"]
                    },{
                        xtype: 'datefield',
                        labelWidth: 30,
                        allowBlank:false,
                        name: 'date_stop',
                        format: 'Y-m-d',
                        margin: '0 10 0 0',
                        fieldLabel: 'По',
                        value: new Date()
                    },{
                        xtype: 'combobox',
                        itemId: 'hours_stop',
                        name : 'hours_stop',
                        allowBlank:false,
                        autoSelect: true,
                        editable: false,
                        labelWidth: 15,
                        width: 70,
                        value: "23",
                        fieldLabel: 'ч.',
                        margin: '0 10 0 0',
                        store:["00","01","02","03","04","05","06","07","08","09","10","11",
                               "12","13","14","15","16","17","18","19","20","21","22","23"]
                    },{
                        xtype: 'combobox',
                        itemId: 'minutes_stop',
                        name : 'minutes_stop',
                        labelWidth: 30,
                        width: 85,
                        value: "45",
                        allowBlank:false,
                        autoSelect: true,
                        editable: false,
                        fieldLabel: 'мин.',
                        margin: '0 40 0 0',
                        store:["00","15","30","45"]
                    },{
                        xtype: 'button',
                        text: 'Обновить',
                        itemId: 'update',
                        padding: '2px 2px 2px 2px',
                        iconCls: 'icon-update',
                        handler: function() {
                            this.up('appAdaptiveReport').updateReport();
                        }
                    }]
                }]
            },{
                xtype: 'panel',
                region: 'center',
                itemId: 'chartarea',
                split: true,
                autoScroll:true
            }]
        });
        this.callParent(arguments);
    },
    getChartNew: function(itemChart,title,fields) {
    	var chartPanel = Ext.create('Ext.panel.Panel', {
            itemId: itemChart+'_panel',
            split: true,
            tbar: [{
	            tooltip: 'Загрузить изображение',
	            iconCls: 'icon-preview',
	            handler: function() {
	            	var chart = this.up('panel').down('chart');
	                Ext.MessageBox.confirm('Подтвердите загрузку', 'Вы действительно хотите загрузить график в виде изображения?', function(choice){
	                    if(choice == 'yes'){
	                        chart.download({
	                            url: '/down_chart/',
                                format: 'png'
	                        });
	                    }
	                });
	            }
	        },{
	            tooltip: 'Экспорт данных',
	            iconCls: 'icon-export_excel',
	            handler: function() {
	                var chart = this.up('panel').down('chart');
	                var formPanel = Ext.create('Ext.form.Panel', {
			            items: []
			        });
	                formPanel.submit({
			            url: '/export_csv/',
			            timeout : 12000,
			            headers: { 'Content-Type': 'application/CSV' },
			            method: 'POST',
			            standardSubmit: true,
			            params:{
			               data_raw : Ext.encode(chart.raw_data)
			            }
			        });
	            }
	        },{
	            tooltip: 'Инвентировать',
	            iconCls: 'icon-chart_clear',
	            handler: function() {
	            	var chart = this.up('panel').down('chart');
	            	var legend = chart.getLegend();
	            	for (var i=0;i<fields.length;i++){
						legend.toggleItem(i);	            		
	            	};
	            	//var nodes = legend.getNodes();
	            	//for(var i=0;i<nodes.length;i++){
	            		//if (! legend.getRecord(nodes[i]).get('disabled')) {
	            		//	legend.toggleItem(i);
	            		//}
	            	//};
	            }
	        }],
            items: [
            {
                xtype: 'chart',
                itemId: itemChart,
                width: 1050,
				height: 500,
	            legend: {
					docked: 'right'
				},
                insetPadding: 40,
                axes: [{
                    type: 'numeric',
		            position: 'left',
		            grid: true,
		            renderer: function(s,v) {
                        return Ext.util.Format.number(v, '0.0');
                    }
		        },{
		            type: 'time',
		            position: 'bottom',
		            fields: ['datetime_start'],
		            grid: true,
		            dateFormat: 'y-m-d'
		        }],
		        sprites: [{
	                type: 'text',
	                text: title,
	                font: '12px Helvetica',
	                width: 100,
	                height: 30,
	                x: 40,
	                y: 20
	            }]
            }]
        });
        return chartPanel;
    },
    getSeriesNew: function(fields) {
    	var series = [];
        for(var i=0;i<fields.length;i++){
	    	var newSeries = {
	            type: 'line',
	            axis: 'left',
	            title: fields[i],
	            xField: 'datetime_start',
	            yField: fields[i],
	            showInLegend: true,
	            //stacked: true,
	            style: {
	                lineWidth: 1
	                //color: this.chartColors[i+1]
	            },
	            marker: {
		            type: 'circle',
		            size: 2,
		            radius: 2,
		            'stroke-width': 0
		        },
	            tips: {
					trackMouse: true,
					width: 200,
					height: 30,
					//padding: '10 10 10 10',
					style: 'background: #fff',
		            renderer: function(toolTip,storeItem, item) {
		                toolTip.setHtml(Ext.util.Format.number(storeItem.get(item.field), '0.0') + ' на: ' + Ext.Date.format(new Date(storeItem.get('datetime_start')), "Y-m-d H:i"));
		            }
	            }
	        };
	        series.push(newSeries);
        };
        return series;
    },
    getFieldsNew: function(fields) {
    	var fields_new = [];
        for(var i=0;i<fields.length;i++){
	    	var newField = {
	    		name: fields[i], 
				convert: function(v) {
					return parseFloat(v);
				}
	    	};
	    	fields_new.push(newField);
	    };
	    fields_new.push({
	    	name:'datetime_start'
	    });
	    	
    	return fields_new;
    },
    updateReport: function() {
    	var my = this;
    	var report_type = my.typeapp;
    	var form = this.down("form");
    	if (!form.isValid()) {
    		Ext.Msg.alert('Предупреждение', 'Заполнены не все поля формы!\n');
            return;
        };
        var mss_id = form.getValues().mss;
        var objects_id = form.getValues().objects;
        var datetime_start = form.getValues().date_start + " " +  form.getValues().hours_start + ":" + form.getValues().minutes_start;
        var datetime_stop = form.getValues().date_stop + " " +  form.getValues().hours_stop + ":" + form.getValues().minutes_stop;
        if (Ext.Date.parse(datetime_start, "Y-m-d H:i")>=Ext.Date.parse(datetime_stop, "Y-m-d H:i")) {
            Ext.Msg.alert('Предупреждение', 'Не верно указан диапазон дат!'); 
            return;
        };
        form.down('#update').setDisabled(true);
        Ext.Ajax.request({
            url: '/reports/',
            params: {
                datetime_start: datetime_start,
                datetime_stop: datetime_stop,
                mss_id: mss_id,
                objects_id: Ext.encode(objects_id),
                report_type: report_type,
                title: this.title
            },
            success: function(response, opts) {
                var obj = Ext.decode(response.responseText);
                var data = obj.messages;
                var chartarea = my.down('#chartarea');
		        chartarea.removeAll(true);
				chartarea.updateLayout();
		        for(var i=0;i<data.length;i++){
			        chartarea.add(my.getChartNew(data[i].chart_id,data[i].title,data[i].fields));
	                var chart = my.down("#"+data[i].chart_id);
	                chart.setStore(new Ext.data.ArrayStore({
	                	fields: my.getFieldsNew(data[i].fields)
	                }));
	                chart.setSeries(my.getSeriesNew(data[i].fields));
	                chart.store.loadData(data[i].data);
	                chart.raw_data = data[i].data;
	             }
                form.down('#update').setDisabled(false);
            },
            failure: function(response, options) {
                Ext.MessageBox.alert('Error', "Ошибка загрузки данных");
                console.log(response,options);
                form.down('#update').setDisabled(false);
            }
        })
    }
})