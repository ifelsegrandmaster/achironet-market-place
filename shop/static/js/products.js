document.addEventListener('DOMContentLoaded', function() {
    // resize all the product items to the maximum size
    let productItems = document.querySelectorAll('.product-item')
        // find the maximum height
    if (productItems.length > 0) {
        let maxHeight = productItems[0].clientHeight
        for (const productItem of productItems) {
            if (productItem.clientHeight > maxHeight)
                maxHeight = productItem.clientHeight
        }
        // now resize each and every client height of all the elements
        for (const productItem of productItems) {
            productItem.style.height = `${maxHeight}px`;
        }
    }

    // also prepare the links so that they will load the appropriate page
    let linkItems = document.querySelectorAll('.page-lin')
    console.log(linkItems)
        // now process the links

    for (const link of linkItems) {
        // get the link item
        link.href = `${link.href}?page=${link.dataset.page}`
    }

    // for search
    // also prepare the links so that they will load the appropriate page
    let linkItemsSearching = document.querySelectorAll('.page-lin-search')
        // now process the links

    for (const link of linkItemsSearching) {
        // get the link item
        link.href = `${link.href}?q=${link.dataset.query}&page=${link.dataset.page}`
    }

    //get the link that connect us to the previous page
    let previousPageLink = document.querySelector('#previous-page')
    if (previousPageLink) {
        // modify the link url
        previousPageLink.href = `${previousPageLink.href}?q=${link.dataset.query}&page=${previousPageLink.dataset.page}`
    }
    //get the link that connect us to the next page
    let nextPageLink = document.querySelector('#next-page')
    if (nextPageLink) {
        // modify the link url
        nextPageLink.href = `${nextPageLink.href}?q=${link.dataset.query}&page=${nextPageLink.dataset.page}`
    }
})