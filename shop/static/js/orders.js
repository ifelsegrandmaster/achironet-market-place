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

function changeStatus(checkBox) {
    let itemId = checkBox.dataset.item
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/admin-dashboard/orders/change-items/`,
        type: 'post',
        data: {
            item_id: itemId
        },
        headers: {
            'X-CSRFToken': csrftoken
        },
        contentType: false,
        processData: false,
        cache: false,
        success: function(response) {
            if (response.success) {
                // now change the checkbox to checked
            } else {
                //uncheck it
            }
        },
        error: function(error) {
            let informationTitle = document.querySelector('#information-title')
            let informationBody = document.querySelector('#information-body')
                // now update these fields and show the dialog
            informationTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error uploading image.'
            informationBody.innerText = "Upload failed: could not upload picture."
            $('#information-dialog').modal('show')
        }
    })
}