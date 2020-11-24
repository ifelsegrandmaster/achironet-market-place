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

// now create the function for sending data to the backend to send emails for the motherfucken
// users
function sendEmails(button) {
    // get the group id
    id = parseInt(button.dataset.group)
    postData(`${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/admin-dashboard/mail-sellers/`, {
            group_id: id
        })
        .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
            if (data.success) {
                // then toggle the information dialog
                // show that an error has happened
                let informationTitle = document.querySelector('#information-title')
                let informationBody = document.querySelector('#information-body')
                    // now update these fields and show the dialog
                informationTitle.innerHTML = 'Success.'
                informationBody.innerText = `${data.message}`
                $('#information-dialog').modal('show')

                if (data.deleteGroup) {
                    $(`#row${data.group_id}`).remove();
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