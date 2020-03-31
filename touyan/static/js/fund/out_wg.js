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

        })
    })
})