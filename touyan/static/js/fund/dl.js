$(function () {
    init()
})

function init() {
    query();
}

function query() {
     getJson('/fund/dl_query',{},function (data) {

     })
}