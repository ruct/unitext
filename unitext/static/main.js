$(document).ready(function () {
    bsCustomFileInput.init()
});

let $form = $('#convert-form');
let $fileInput = $('#convert-input-file');
$form.submit(event => {
    event.preventDefault();

    let $format = $form.find(':checked');

    let files = $fileInput.prop('files');
    if (files.length === 0) {
        console.log('No file selected!');
        return;
    }

    if ($format.length === 0) {
        console.log('No format selected!');
        return;
    }

    let formData = new FormData($form.get(0));
    let formatName = formData.get('format');
    fetch(`/convert/${formatName}`, {
        method: 'POST',
        body: formData
    }).then(response => {
        return response.blob()
    }).then(blob => {
        download(blob, 'File.ext');
    }).catch(error => {
        console.log(`Something went wrong ${error}`);
    })
});