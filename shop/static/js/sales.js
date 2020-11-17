// What happens is that an ajax request is made to the endpoint to fetch sales data
// Only get requests are allowed not post
// On success, then draw a chart on the page using chartjs.
// If an error happens show that an error has happened and data can't be displayed

const hostname = "localhost:8000"

document.addEventListener("DOMContentLoaded", function() {
    //Make a request
    fetch(`http://${hostname}/sell/fetch-revenue-data/`)
        .then(response => response.json())
        .then(data => {
            salesData = JSON.parse(data.data)
            console.log(salesData)
                // Now prepare the data for the chart
            let months = []
            let sales_made = []
            let products_sold = []
                //now iterate the sales data and append data to the arrays
            for (const sale of salesData) {
                months.push(sale.month);
                sales_made.push(sale.sales);
                products_sold.push(sale.products_sold);
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
                        backgroundColor: [
                            'rgba(99, 255, 132, 0.2)',
                        ],
                        borderColor: [
                            'rgba(99, 255, 132, 1)'
                        ],
                        borderWidth: 1
                    }, {
                        label: 'Products sold ',
                        data: products_sold,
                        backgroundColor: [
                            'rgba(132, 99, 255, 0.2)',
                        ],
                        borderColor: [
                            'rgba(132, 99, 255, 1)',
                        ],
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
        });
})