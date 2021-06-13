// https://stackoverflow.com/questions/46752209/how-render-template-after-post-data-with-ajax-in-flask/46752440
$('#trigger-search').click(function () {
    let value = $('#search-keyword').val()
    if (value.length > 0) {
        let keyword = $('#search-keyword').val()
        window.location.href = '/search/' + keyword;
    }
})
$(function () {
    $('#search-keyword').keypress(function (e) {
        if (e.which == 13) {
            //dosomething
            let value = $('#search-keyword').val()
            console.log(value)
            if (value.length > 0) {
                let keyword = $('#search-keyword').val()
                window.location.href = '/search/' + keyword;
            }
        }
    })
})