$('#specification-form').submit(function() {
        // now take all the values created by the user and
        // assign to the form hidden input element
        let attributes = []
        let attributeRows = document.querySelectorAll("#attributes-table tbody tr")
        console.log(attributeRows)
            //now attributes rows have been selected now select the cells
        for (const attributeRow of attributeRows) {
            //select all the cells
            console.log(attributeRow)
            let cell1 = attributeRow.getElementsByTagName('td')[0]
            let cell2 = attributeRow.getElementsByTagName('td')[1]
                // now access the input element
            keyInputElement = cell1.getElementsByTagName('input')[0]
            valueInputElement = cell2.getElementsByTagName('input')[0]

            let attribute = {
                key: keyInputElement.value,
                value: valueInputElement.value
            }
            attributes.push(attribute)
        }

        attributesString = JSON.stringify(attributes)
        console.log(attributesString)
            // get the the attributes hidden input
        attributesInput = document.querySelector('#id_attributes')
        attributesInput.value = attributesString

        return true
    })
    // Create a new row for adding attributes of a product
function addNewAttribute() {
    let tbodyRef = document.getElementById('attributes-table').getElementsByTagName('tbody')[0];
    let newAttributeRow = tbodyRef.insertRow()
    let cell1 = newAttributeRow.insertCell()
    let cell2 = newAttributeRow.insertCell()
    let cell3 = newAttributeRow.insertCell()

    //Append an input element to cell1
    var inputKey = document.createElement('input')
    inputKey.type = 'text'
    inputKey.className = 'form-control key'
    inputKey.id = 'key'
    inputKey.placeholder = 'Property'
    inputKey.required = true
    cell1.appendChild(inputKey)
        //Append an input element to cell1
    var inputValue = document.createElement('input')
    inputValue.type = 'text'
    inputValue.className = 'form-control value'
    inputValue.placeholder = 'Value'
    inputValue.required = true
    inputValue.id = 'value'
    cell2.appendChild(inputValue)

    //Append remove button to cell3
    cell3.innerHTML = '<span onclick="deleteAttribute(this)" class="ctrl-attribute"><i class="fas fa-minus-circle"></i> Remove</span>'
}



function deleteAttribute(elem) {
    elem.parentNode.parentNode.remove()
}