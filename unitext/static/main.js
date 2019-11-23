$(document).ready(function () {
    bsCustomFileInput.init()
});


let $errorMessage = $('#error-message');
let $form = $('#convert-form');
let $fileInput = $('#convert-input-file');
let $formatType = $('input[type=radio]');

$fileInput.change(() => {
    $errorMessage.hide();
});

$formatType.change(() => {
    $errorMessage.hide();
});

$form.submit(event => {
    event.preventDefault();
    $errorMessage.hide();

    let $format = $form.find(':checked');

    let files = $fileInput.prop('files');
    if (files.length === 0) {
        $errorMessage.text('No file selected!').show();
        return;
    }

    if ($format.length === 0) {
        $errorMessage.text('No format selected!').show();
        return;
    }

    let formData = new FormData($form.get(0));
    let formatName = formData.get('format');
    fetch(`/convert/${formatName}`, {
        method: 'POST',
        body: formData
    }).then(response => {
        if (!response.ok) {
            response.json().then(json => {
                $errorMessage.text(json['error']);
                $errorMessage.show();
            }).catch(() => {
                $errorMessage.text('Unknown error occurred').show();
            })
        } else {
            response.blob().then(blob => {
                const contentDispositionHeader = 'Content-Disposition';
                let filename = 'converted-file';
                if (response.headers.has(contentDispositionHeader)) {
                    let header = response.headers.get('Content-Disposition');
                    let match = header.match(/filename="(.+)"/);
                    if (match) {
                        filename = match[1];
                    }
                }

                const contentTypeHeader = 'Content-Type';
                let contentType = undefined;
                if (response.headers.has(contentType)) {
                    contentType = response.headers.get(contentTypeHeader);
                }

                download(blob, filename, contentType);
            })
        }
    }).catch(error => {
        $errorMessage.text(`Something went wrong: ${error}`).show();
    });
});