function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(function() {

    /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
    $("#id_file").change(function() {
        // ...
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image()
                img.onload = function() {
                        if (this.width >= 512 && this.height >= 512) {
                            // this image has valid dimensions
                            $("#image").attr("src", e.target.result);
                            $("#modalCrop").modal("show");
                        } else {
                            let informationTitle = document.querySelector('#information-title')
                            let informationBody = document.querySelector('#information-body')
                                // now update these fields and show the dialog
                            informationTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Your image is very small.'
                            informationBody.innerText = "You need to select a image which width and height which is greater or equal to 512 pixels."
                            $('#information-dialog').modal('show')
                        }
                    }
                    // trigger the onload event
                img.src = e.target.result

            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* SCRIPTS TO HANDLE THE CROPPER BOX */
    var $image = $("#image");
    var $mobileImage = $("#on-mobile-image");
    var cropBoxData;
    var canvasData;

    // if this is a mobile device just put simple user interface
    // keep it simple you won't die

    function cropImageOnMobileDevice() {
        // now show some user interface for mobile device
        $("#mobile-cropper").show()
            // now the user interface shown next build the logic
            // init cropper
        $mobileImage.cropper({
            viewMode: 2,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 512,
            minCropBoxHeight: 512,
            minCanvasWidth: 200,
            minCanvasHeight: 200,
            minContainerWidth: 200,
            minContainerHeight: 200,
            ready: function() {
                $mobileImage.cropper("setCanvasData", canvasData);
                $mobileImage.cropper("setCropBoxData", cropBoxData);
            }
        });

        // prepare data and start uploading
    }

    $('.js-mobile-crop-and-upload').click(function() {
        // first clean up
        cropBoxData = $mobileImage.cropper("getCropBoxData");
        canvasData = $mobileImage.cropper("getCanvasData");
        $mobileImage.cropper("destroy");
        $("#mobile-cropper").hide()
            // set the data
        var cropData = $mobileImage.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        // create a new form data object
        $("#formUpload").submit();
    })

    // enable zoom in button
    $(".mobile-js-zoom-in").click(function() {
        $mobileImage.cropper("zoom", 0.1)
    });

    // enable zoom out
    $(".mobile-js-zoom-out").click(function() {
        $mobileImage.cropper("zoom", -0.1)
    });

    var cropperHeight = 400;
    var cropperWidth = 400;
    var cropperBoxWidth = 512;
    var cropperBoxHeight = 512;

    if (window.mobileCheck) {
        cropperHeight = 200;
        cropperWidth = 200;
        cropperBoxHeight = 200;
        cropperBoxHeight = 200;
    }

    $("#modalCrop").on("show.bs.modal", function() {
        $image.cropper({
            viewMode: 2,
            aspectRatio: 1 / 1,
            minCropBoxWidth: cropperBoxWidth,
            minCropBoxHeight: cropperBoxHeight,
            minCanvasWidth: cropperWidth,
            minCanvasHeight: cropperHeight,
            minContainerWidth: cropperWidth,
            minContainerHeight: cropperHeight,
            ready: function() {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function() {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    })

    // enable zoom in button
    $(".js-zoom-in").click(function() {
        $image.cropper("zoom", 0.1)
    });

    // enable zoom out
    $(".js-zoom-out").click(function() {
        $image.cropper("zoom", -0.1)
    });


    //form upload
    $("#formUpload").submit(function(e) {
        e.preventDefault();
        $form = $(this)
        var fd = new FormData(this);
        $.ajax({
            url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/users/upload/photos/`,
            type: 'post',
            data: fd,
            headers: {
                'X-CSRFToken': csrftoken
            },
            contentType: false,
            processData: false,
            beforeSend: function() {
                $("#loader").modal("show");
            },
            cache: false,
            success: function(response) {
                $("#loader").modal("hide");
                $("#profile_pic").attr("src", response.url);
                $("#id_profile_picture").val(response.photo_id);
            },
            error: function(error) {
                $("#loader").modal("hide");
                $('#information-title').html('<i class="fas fa-exclamation-triangle"></i> Error uploading picture.')
                $('#information-body').text("Upload failed: could not upload picture.")
                $('#information-dialog').modal('show')
            }
        })
    })

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function() {
        $("#modalCrop").modal("hide");
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        // create a new form data object
        $("#formUpload").submit();
    });

});