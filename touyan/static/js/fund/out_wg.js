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
        getJson('/fund/wg_query',{},function (data) {
            if(data['errCode'] != '200'){
                alert(data['errMsg']);
                return
            }
            fillCharts(data['data'])
        })
    })
})

function fillCharts(data) {
    var div = 0;
    for(var c in data){
        div++;
        $('#charts').append('    <div class="col-xs-12">\n' +
            '        <div id="chart_'+ div.toString() +'" style="margin-left: 0px;width: 100%;height:100%;min-height:400px;min-width:300px;margin-top: 20px;"></div>\n' +
            '    </div>')

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

        var option = {
            title: {
                left: 'center',
                text: data[c]['name'] + c + '('+data[c]['nowtime'] +')',
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
            grid:{
            },
            xAxis: [
                {
                    type: 'category',
                    data: data[c]['data']['day'],
                    axisPointer: {
                        type: 'shadow'
                    },
                    boundaryGap: false,
                }
            ],
            yAxis: [
                {
                    type: 'value',
                    name: '',
                    axisLabel: {
                        formatter: '{value}'
                    },
                    scale:true,

                },
            ],
            dataZoom: [
                {
                    type: 'inside',
                    xAxisIndex: [0],
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
                    }
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
                    }

                },
            ]
        };
        var seasonCharts = echarts.init(document.getElementById('chart_'+div.toString()));
        seasonCharts.setOption(option, true);
        seasonCharts.resize();
    }
}