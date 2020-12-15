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

//function to perform post request
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

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
    let messageText = document.querySelector('#message-text').value
        // The PROTOCOL  and HOSTNAME constants are found in the file "constants.js"
    postData(`${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/shop/publishing/products/`, {
            product_id: id,
            message_text: messageText
        })
        .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
            if (data.success) {
                // then update the button element and show notification that
                // a product has been approved
                // or disapproved
                btn = document.querySelector(`#btn-moderate${data.product_id}`)
                if (data.published) {
                    // update
                    btn.innerHTML = '<i class="fas fa-times"></i> Disapprove'
                } else {
                    btn.innerHTML = '<i class="fas fa-check"></i> Approve'
                }
            }
        }).catch(error => {
            // show that an error has happened
            let informationTitle = document.querySelector('#information-title')
            let informationBody = document.querySelector('#information-body')
                // now update these fields and show the dialog
            informationTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error moderating product.'
            informationBody.innerText = "An error happened, could not change product status."
            $('#information-dialog').modal('show')
        })
}