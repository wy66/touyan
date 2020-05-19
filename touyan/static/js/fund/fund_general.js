$(function () {
    init();
})


function init() {
    query();
}

function query() {
    var day = $('#dayrank').val();
    if(day == ''){
        alert('日期不能为空');
        return
    }
    getJson('/fund/fund_general_query',{'day':day},function (data) {
        if(data['errCode'] != '200'){
            alert(data['errMsg']);
            return
        }
        var columnsInit = [[{field: '', title: data['data']['days'][0] + '    ' + data['data']['days'][0], align: 'center',valign: 'middle',colspan:2},],
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
                var day = $('#dayrank').val();
                if(day == ''){
                    alert('日期不能为空');
                    return
                }
                getJson('/fund/fund_general_rank',{'sname':row['sname'],'day':day},function (data) {
                    fillCharts(data['data']);
                })
            }

        })
    })
}