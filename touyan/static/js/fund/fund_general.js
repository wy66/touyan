$(function () {
    init();
})


function init() {
    query();
}

function query() {
    getJson('/fund/fund_general_query',{},function () {

    })
}