// What happens is that an ajax request is made to the endpoint to fetch sales data
// Only get requests are allowed not post
// On success, then draw a chart on the page using chartjs.
// If an error happens show that an error has happened and data can't be displayed


document.addEventListener("DOMContentLoaded", function() {
    //Make a request
    /*
    fetch(`${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/sell/fetch-revenue-data/`)
        .then(response => response.json())
        .then(data => {
            salesData = JSON.parse(data.data)
            console.log(salesData)
                // Now prepare the data for the chart
            let months = []
            let sales_made = []
            let products_sold = []
            let sales_colors = []
            let products_colors = []
                //now iterate the sales data and append data to the arrays
            for (const sale of salesData) {
                months.push(sale.month);
                sales_made.push(sale.sales);
                products_sold.push(sale.products_sold);
                products_colors.push('rgba(132, 99, 255, 1)')
                sales_colors.push('rgba(99, 255, 132, 1)')
            }
            //now draw the chart
            var ctx = document.getElementById('sales-chart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Sales $',
                        data: sales_made,
                        backgroundColor: sales_colors,
                        borderColor: sales_colors,
                        borderWidth: 1
                    }, {
                        label: 'Products sold ',
                        data: products_sold,
                        backgroundColor: products_colors,
                        borderColor: products_colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        }); */
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/sell/fetch-revenue-data/`,
        type: 'get',
        contentType: false,
        processData: false,
        cache: false,
        success: function(response) {
            console.log(response)
            salesData = JSON.parse(response.data)
            console.log(salesData)
                // Now prepare the data for the chart
            let months = []
            let sales_made = []
            let products_sold = []
            let sales_colors = []
            let products_colors = []
                //now iterate the sales data and append data to the arrays
            for (const sale of salesData) {
                months.push(sale.month);
                sales_made.push(sale.sales);
                products_sold.push(sale.products_sold);
                products_colors.push('rgba(132, 99, 255, 1)')
                sales_colors.push('rgba(99, 255, 132, 1)')
            }
            //now draw the chart
            var ctx = document.getElementById('sales-chart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Sales $',
                        data: sales_made,
                        backgroundColor: sales_colors,
                        borderColor: sales_colors,
                        borderWidth: 1
                    }, {
                        label: 'Products sold ',
                        data: products_sold,
                        backgroundColor: products_colors,
                        borderColor: products_colors,
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        },
        error: function(error) {
            let informationTitle = document.querySelector('#information-title')
            let informationBody = document.querySelector('#information-body')
                // now update these fields and show the dialog
            informationTitle.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error loading sales chart.'
            informationBody.innerText = "Could not get sales data from the server."
            $('#information-dialog').modal('show')
        }
    })
})