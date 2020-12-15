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


function shipOrder(id) {
    let orderId = id
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/admin-dashboard/orders/ship-order/`,
        type: 'post',
        data: JSON.stringify({
            order_id: orderId
        }),
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': "application/json"
        },
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
            if (response.success) {
                // now change the shipped status
                if (response.shipped) {
                    // update the user interface
                    $("#shipped-status").removeClass("fa-times")
                    $("#shipped-status").addClass("fa-check")
                    $("#ship-order-btn").text("Undo ship")
                } else {
                    $("#shipped-status").removeClass("fa-check")
                    $("#shipped-status").addClass("fa-times")
                    $("#ship-order-btn").text("Ship order")
                }
            } else {
                // maybe the order is not ready to be shipped
                if (response.not_ready) {
                    $('#information-title').html('<i class="fas fa-exclamation-triangle"></i> Could not ship this order.')
                    $('#information-body').text("Order is not ready to be shipped.")
                    $('#information-dialog').modal('show')
                }
            }
        },
        error: function(error) {
            $('#information-title').html('<i class="fas fa-exclamation-triangle"></i> Operation failed.')
            $('#information-body').text("Could not change status of the order.")
            $('#information-dialog').modal('show')
        }
    })
}