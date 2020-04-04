$(function () {
    $('#add').click(function () {
        var code = $('#code').val();
        var sdate = $('#sdate').val();
        getJson('/fund/wg_add',{'code':code,'sdate':sdate},function (data) {
            if(data['errCode'] != '200'){
                alert(data['errMsg']);
                return
            }

        })
    })
    
    $('#search').click(function () {
        queryTable();
    })
    init();

})

function queryTable() {
    getJson('/fund/wg_query_table',{},function (data) {
         if(data['errCode'] != '200'){
            alert(data['errMsg']);
            return
        }
        fillTable(data['table'])
    })
}

function query() {
     getJson('/fund/wg_query',{},function (data) {
        if(data['errCode'] != '200'){
            alert(data['errMsg']);
            return
        }
        fillTable(data);
        fillCharts(data['data'])
    })
}

function init() {
    queryTable();
}

function fillTable(data) {
 var columnsInit = [
    [
        {field: 'code', title: '代码', align: 'center',valign: 'middle',},
        {field: 'sdate', title: '基准开始日期', align: 'center',valign: 'middle'},
        {field: 'name', title: '全称', align: 'center',valign: 'middle',},
        {field: 'short_name', title: '简称', align: 'center',valign: 'middle'},
    ]
 ];
    $('#table1').bootstrapTable('destroy').bootstrapTable({
        striped: true,
        columns: columnsInit,
        data: data,
        onDblClickRow:function (row) {
             getJson('/fund/wg_query',{'code':row['code'],'sdate':row['sdate'],'name':row['short_name']},function (data) {
                query();
            })
        }

    })
}

function fillCharts(data) {
    var div = 0;
    $('#charts').empty();
    for(var c in data){
        div++;
        $('#charts').append('    <div class="col-xs-12">\n' +
            '        <div id="chart_'+ div.toString() +'" style="margin-left: 0px;width: 100%;height:100%;min-height:600px;min-width:300px;margin-top: 20px;"></div>\n' +
            '    </div>')

        //y轴平行x轴格子线
        var markdata = []
        for(var i = 0;i<data[c]['markline'].length;i++){
            markdata.push(
                {
                    'name':data[c]['markline'][i],
                    'yAxis':data[c]['markline'][i],

                }
            )
        }
        markdata.push(
            {
                'name':'基准',
                'yAxis':data[c]['base_value'],
                'lineStyle': {
                    'color': 'red'
                }
            }
        )

        //买卖及起始点位
        var markpoins = [];
        for(var i = 0;i<data[c]['bs'].length;i++){
            var name = ''
            if(data[c]['bs'][i]['act'] == 'buy'){
                markpoins.push(
                    {
                        name: '买',
                        coord: [data[c]['bs'][i]['sdate'], data[c]['bs'][i]['sum_value']],
                        symbolRotate:180,
                        itemStyle:{
                            color:'#009933'
                        }
                    }
                )
            }else {
                markpoins.push(
                    {
                        name: '卖',
                        coord: [data[c]['bs'][i]['sdate'], data[c]['bs'][i]['sum_value']],

                        itemStyle:{
                            color:'#dd2200',

                        },
                    }
                )
            }
        }

        var option = {
            title: {
                left: 'center',
                text: data[c]['name'] +' ('+ c +') '+ '('+data[c]['nowtime'] +')',
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    crossStyle: {
                        color: '#999'
                    }
                }
            },
            legend: {
                left: 'center',
                top:'8%',
                data: ['单位净值','累计净值',]
            },
        grid:  [{
            left: '10%',
            right: '10%',
            bottom: 200
        },
        {
            left: '10%',
            right: '10%',
            height: 80,
            bottom: 80
        }],
            xAxis: [
                {
                    type: 'category',
                    data: data[c]['data']['sdate'],
                    axisPointer: {
                        type: 'shadow'
                    },
                    boundaryGap: false,
                    gridIndex:0,
                },
                {
                    type: 'category',
                    data: data[c]['macd']['day'],
                    axisPointer: {
                        type: 'shadow'
                    },
                    boundaryGap: false,
                    gridIndex:1,
                },
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '',
                    axisLabel: {
                        formatter: '{value}'
                    },
                    scale:true,
                    gridIndex:0,

                },
                                {
                    type: 'value',
                    name: '',
                    axisLabel: {
                        formatter: '{value}'
                    },
                    scale:true,
                    gridIndex:1,
                },
            ],
            dataZoom: [
                {
                    type: 'inside',
                    xAxisIndex: [0,1],
                    start: 80,
                    end: 100
                },
            ],
            series:[
                {
                    name: '单位净值',
                    type: 'line',
                    data:data[c]['data']['net_value'],
                    symbol:"none",
                    itemStyle: {
                        normal: {

                        }
                    },
                },
                {
                    name: '累计净值',
                    type: 'line',
                    symbol:"none",
                    data: data[c]['data']['sum_value'],
                    itemStyle: {
                        normal: {
                        }
                    },
                    markLine:{
                        data:markdata,
                    },

                    markPoint:{
                        data:markpoins,
                        label:{
                            formatter:function(parms){
                                return parms.data.name
                            }
                        },
                    }

                },
                {
                    name: 'DIF',
                    type: 'line',
                    data:data[c]['macd']['diff'],
                    symbol:"none",
                    itemStyle: {
                        normal: {
                            color:'#ff9100'
                        }
                    },
                    xAxisIndex: 1, yAxisIndex: 1
                },
                                {
                    name: 'DEA',
                    type: 'line',
                    data:data[c]['macd']['dea'],
                    symbol:"none",
                    itemStyle: {
                        normal: {
                            color:'#1c77d2'
                        }
                    },
                    xAxisIndex: 1, yAxisIndex: 1
                },
                {
                    name: 'macd',
                    type: 'bar',
                    data:data[c]['macd']['bar'],
                    symbol:"none",
                    itemStyle: {
                        normal: {
                             color:function (value) {
                                if(value.value>=0){
                                    return '#CD0000'
                                }else{
                                    return '#548B54'
                                }
                            }
                        }
                    },
                    xAxisIndex: 1, yAxisIndex: 1
                },
            ]
        };
        var seasonCharts = echarts.init(document.getElementById('chart_'+div.toString()));
        seasonCharts.setOption(option, true);
        seasonCharts.resize();
    }
}