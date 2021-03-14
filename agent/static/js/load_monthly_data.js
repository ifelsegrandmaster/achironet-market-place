$(document).ready(function() {
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/agent/fetch-commission-data/`,
        type: 'get',
        contentType: false,
        processData: false,
        cache: false,
        success: function(response) {
            console.log(response)
                //Monthly data
            monthly_commission = JSON.parse(response.monthly_data)
            console.log(monthly_commission)
                // Now prepare the data for the chart
            let monthly_days = []
            let monthly_commission_made = []
            let monthly_commission_colors = []
                //now iterate the sales data and append data to the arrays
            for (const day of monthly_commission) {
                monthly_days.push(day.day);
                monthly_commission_made.push(day.amount);
                monthly_commission_colors.push('rgba(99, 255, 132, 1)');
            }
            //now draw the chart
            var ctx = document.getElementById('monthly-chart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: monthly_days,
                    datasets: [{
                        label: 'Commission $',
                        data: monthly_commission_made,
                        backgroundColor: monthly_commission_colors,
                        borderColor: monthly_commission_colors,
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
            // now update these fields and show the dialog
            $('#information-title').html('<i class="fas fa-exclamation-triangle"></i> An error occured.')
            $('#information-body').text("Could not get data from the server.")
            $('#information-dialog').modal('show')
        }
    })
})