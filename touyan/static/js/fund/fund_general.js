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
    if(daynum == ''){
        alert('不能为空');
        return
    }
    var sdate = $('#sdate').val();
    if(sdate == ''){
        alert('不能为空');
        return
    }
    getJson('/fund/fund_general_query',{'daynum':daynum,'sdate':sdate},function (data) {
        if(data['errCode'] != '200'){
            alert(data['errMsg']);
            return
        }
        var columnsInit = [[{field: '', title: data['data']['days'][0] + '    ' + data['data']['days'][1], align: 'center',valign: 'middle',colspan:2},],
            [
                {field: 'sname', title: '代码', align: 'center',valign: 'middle',},
                {field: 'chg', title: '涨跌幅', align: 'center',valign: 'middle',sortable:true},

            ]
        ];
        $('#table').bootstrapTable('destroy').bootstrapTable({
            striped: true,
            columns: columnsInit,
            data: data['data']['table'],
            onDblClickRow:function (row) {
                var daynum = $('#daynum').val();
                if(daynum == ''){
                    alert('日期不能为空');
                    return
                }
                 $('#myModal').modal('show');
                    getJson('/fund/fund_general_rank',{'sname':row['sname'],'daynum':daynum},function (data) {
                    if(data['errCode'] != '200'){
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
            text: data['name'],
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
            data: ['净值','排名(右)'],
        },
        grid: {},
        xAxis: [
            {
                type: 'category',
                data: data['charts']['xlist'],
                axisPointer: {
                    type: 'shadow'
                },
            }
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
                splitLine:{
                    show:false
                }
            },
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0],
                start: 0,
                end: 100
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
                name: '排名(右)',
                type: 'line',
                data: data['charts']['rank'],
                yAxisIndex:1,
                itemStyle: {
                    normal: {
                        color: '#CD0000',
                    }
                },
            },

        ]
    };
    var seasonCharts = echarts.init(document.getElementById('charts1'));
    seasonCharts.setOption(option, true);
    seasonCharts.resize();
}