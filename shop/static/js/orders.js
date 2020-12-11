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
    console.log("This item id", itemId)
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/admin-dashboard/orders/change-items/`,
        type: 'post',
        data: JSON.stringify({
            item_id: itemId
        }),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': "application/json"
        },
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
            console.log(response)
            if (response.success) {
                // now change the checkbox to checked
            } else {
                //uncheck it
                checkBox = $(`#checkbox-for-item-${itemId}`)
                checkBox.prop("checked", false)
            }
        },
        error: function(error) {
            let informationTitle = document.querySelector('#information-title')
            let informationBody = document.querySelector('#information-body')
                // now update these fields and show the dialog
            informationTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Operation failed.'
            informationBody.innerText = "Could not change status of the item."
            $('#information-dialog').modal('show')
        }
    })
}