

function getNDay(num) {
    var now = new Date();
    var datenum = new Date(now.getTime() - (num * 24 * 60 * 60 * 1000));
    return datenum.getFullYear() + "-" + ((datenum.getMonth() + 1) < 10 ? "0" : "") + (datenum.getMonth() + 1) + "-" + (datenum.getDate() < 10 ? "0" : "") + datenum.getDate()
}

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
function getJsonSyn(url, data, callback, method, dataType, async) {
    method = method || 'POST';
    dataType = dataType || 'json';
    async = async || false; //默认异步
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
