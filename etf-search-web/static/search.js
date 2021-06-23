// https://stackoverflow.com/questions/46752209/how-render-template-after-post-data-with-ajax-in-flask/46752440
$('#trigger-search').click(function () {
    let value = $('#search-keyword').val()
    if (value.length > 0) {
        let keyword = $('#search-keyword').val()
        window.location.href = '/search/' + keyword;
    }
});

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
});

let autocompleteresult = [];

$(function () {
    let cache = {};
    $("#search-keyword").autocomplete({
        source: function (request, response) {
            let term = request.term;
            console.log(term)
            if (term in cache) {
                response(cache[term] );
                return;
            }
            var xhr = new XMLHttpRequest();
            xhr.responseType='json';
            let keyword = $("#search-keyword").val();
            xhr.open("GET", "/autocomplete/" + keyword, true);
            xhr.send();
            xhr.onload = function () {
                // xhr 객체의 status 값을 검사한다.
                if (xhr.status === 200) {
                    cache[term] = xhr.response;
                    response(xhr.response);
                }
            }
        }
    });
});