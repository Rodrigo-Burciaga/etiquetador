$(function () {

    let bar = $(".bar");
    let percent = $('.percent');
    let status = $("#status");

    $('form').ajaxForm({
        beforeSend: function () {
            status.empty();
            let percentVal = '0%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        uploadProgress: function (event, position, total, percentComplete) {
            let percentVal = percentComplete + '%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        complete: function (xhr) {
            status.html(xhr.responseText);
        }
    });
});

$(function () {
    $('input:file').change(
        function () {
            if ($(this).val()) {
                $('input:submit').attr('disabled', false);
            }
        }
    );
});

