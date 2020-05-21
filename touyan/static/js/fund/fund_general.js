$(function () {
    $('#search').click(function () {
        query();
    })

    init();
})


function init() {
    $('#sdate').val(getNDay(0));
    query();
}

function query() {
    var daynum = $('#daynum').val();
    if (daynum == '') {
        alert('不能为空');
        return
    }
    var sdate = $('#sdate').val();
    if (sdate == '') {
        alert('不能为空');
        return
    }
    getJson('/fund/fund_general_query', {'daynum': daynum, 'sdate': sdate}, function (data) {
        if (data['errCode'] != '200') {
            alert(data['errMsg']);
            return
        }
        var columnsInit = [[{
            field: '',
            title: data['data']['days'][0] + '    ' + data['data']['days'][1],
            align: 'center',
            valign: 'middle',
            colspan: 2
        },],
            [
                {field: 'sname', title: '代码', align: 'center', valign: 'middle',},
                {field: 'chg', title: '涨跌幅', align: 'center', valign: 'middle', sortable: true},

            ]
        ];
        $('#table').bootstrapTable('destroy').bootstrapTable({
            striped: true,
            columns: columnsInit,
            data: data['data']['table'],
            onDblClickRow: function (row) {
                var daynum = $('#daynum').val();
                if (daynum == '') {
                    alert('日期不能为空');
                    return
                }
                $('#myModal').modal('show');
                getJson('/fund/fund_general_rank', {'sname': row['sname'].split('(')[0], 'daynum': daynum}, function (data) {
                    if (data['errCode'] != '200') {
                        alert(data['errMsg']);
                        return
                    }
                    fillCharts(data['data']);
                })
            }

        })
    })
}

function fillCharts(data) {
    var option = {
        title: {
            left: 'center',
            text: data['name'] + '   '+data['newtime'],
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
        toolbox: {
            feature: {
                saveAsImage: {show: true}
            }
        },
        legend: {
            left: 'center',
            top: '8%',
            data: ['净值', '均值', '排名(右)'],
        },
        grid: [{
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
                data: data['charts']['xlist'],
                axisPointer: {
                    type: 'shadow'
                },
                boundaryGap: false,
                gridIndex: 0,
            },
            {
                type: 'category',
                data: data['macd']['day'],
                axisPointer: {
                    type: 'shadow'
                },
                boundaryGap: false,
                gridIndex: 1,
            },
        ],
        yAxis: [
            {
                type: 'value',
                name: '',
                axisLabel: {
                    formatter: '{value}'
                },
                scale: true,
            },
            {
                type: 'value',
                name: '',
                axisLabel: {
                    formatter: '{value}'
                },
                scale: true,
                splitLine: {
                    show: false
                }
            },
            {
                type: 'value',
                name: '',
                axisLabel: {
                    formatter: '{value}'
                },
                scale: true,
                gridIndex: 1,
            },
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0],
                start: 0,
                end: 100,
                xAxisIndex: [0, 1]
            },
        ],
        series: [
            {
                name: '净值',
                type: 'line',
                data: data['charts']['net'],
                itemStyle: {
                    normal: {
                        color: '#5b9bd5',
                    }
                },
            },
            {
                name: '均值',
                type: 'line',
                data: data['charts']['ma'],
                itemStyle: {
                    normal: {
                        color: '#548B54',
                    }
                },
            },
            {
                name: '排名(右)',
                type: 'line',
                data: data['charts']['rank'],
                yAxisIndex: 1,
                itemStyle: {
                    normal: {
                        color: '#CD0000',
                    }
                },
            },

            {
                name: 'DIF',
                type: 'line',
                data: data['macd']['diff'],
                symbol: "none",
                itemStyle: {
                    normal: {
                        color: '#ff9100'
                    }
                },
                xAxisIndex: 1, yAxisIndex: 2
            },
            {
                name: 'DEA',
                type: 'line',
                data: data['macd']['dea'],
                symbol: "none",
                itemStyle: {
                    normal: {
                        color: '#1c77d2'
                    }
                },
                xAxisIndex: 1, yAxisIndex: 2
            },
            {
                name: 'macd',
                type: 'bar',
                data: data['macd']['bar'],
                symbol: "none",
                itemStyle: {
                    normal: {
                        color: function (value) {
                            if (value.value >= 0) {
                                return '#CD0000'
                            } else {
                                return '#548B54'
                            }
                        }
                    }
                },
                xAxisIndex: 1, yAxisIndex: 2
            },

        ]
    };
    var seasonCharts = echarts.init(document.getElementById('charts1'));
    seasonCharts.setOption(option, true);
    seasonCharts.resize();
}