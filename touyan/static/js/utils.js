
function getJson(url, data, callback, method, dataType, async) {
    method = method || 'POST';
    dataType = dataType || 'json';
    async = async || true; //默认异步
    jQuery('#content').showLoading();
    $.ajax({
        url: url,
        method: method,
        data: data,
        dataType: dataType,
        traditional: true,
        async: async,
        success: function (data) {
            jQuery('#content').hideLoading();
            callback(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            jQuery('#content').hideLoading();
            console.log(textStatus);
            console.log(errorThrown);
        }
    })
}
