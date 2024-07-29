$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#processedImage').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#processedImage').hide();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling API /detect_objects
        $.ajax({
            type: 'POST',
            url: '/detect_objects',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (response) {
                // Display the processed image
                console.log(response);
                $('#processedImage').attr('src', response.processed_image_url);
                $('#processedImage').show(); // Ensure the processed image is shown

                // Hide loader
                $('.loader').hide();
                console.log('Success!');
            },
            error: function (xhr, status, error) {
                // Handle error
                console.log(xhr.responseText);
            }
        });
    });
});