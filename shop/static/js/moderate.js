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



function moderateProduct(id) {
    // now make a post request
    // store the product id
    let productIdStore = document.querySelector('#product-id')
    let messageTextStore = document.querySelector('#message-text')
    messageTextStore.value = ""
    productIdStore.value = id
    $('#message-seller-modal').modal('show')
}

function sendMessage() {
    // get the id of the product
    $('#message-seller-modal').modal('hide')
    let productIdStore = document.querySelector('#product-id')
    id = parseInt(productIdStore.value)
        // get the message
    let messageText = document.querySelector('#message-text').value;
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/shop/publishing/products/`,
        type: 'post',
        contentType: "application/json",
        data: JSON.stringify({
            product_id: id,
            message_text: messageText
        }),
        headers: {
            'X-CSRFToken': csrftoken
        },
        processData: false,
        beforeSend: function() {
            $("#loader").modal("show");
        },
        cache: false,
        success: function(response) {
            $("#loader").modal("hide");
            if (response.success) {
                // then update the button element and show notification that
                // a product has been approved
                // or disapproved
                btn = document.querySelector(`#btn-moderate${response.product_id}`)
                if (response.published) {
                    // update
                    btn.innerHTML = '<i class="fas fa-times"></i> Disapprove'
                } else {
                    btn.innerHTML = '<i class="fas fa-check"></i> Approve'
                }
            }
        },
        error: function(error) {
            $("#loader").modal("hide");
            $('#information-title').html('<i class="fas fa-exclamation-triangle"></i> Error moderating product.')
            $('#information-body').text("Could not change product status.")
            $('#information-dialog').modal('show')
        }
    })
}