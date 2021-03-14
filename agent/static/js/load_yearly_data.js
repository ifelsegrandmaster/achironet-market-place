$(document).ready(function() {
    $.ajax({
        url: `${ACHIRONET_PROTOCOL}://${ACHIRONET_HOSTNAME}/agent/fetch-yearly-commission-data/`,
        type: 'get',
        contentType: false,
        processData: false,
        cache: false,
        success: function(response) {
            console.log(response)
            yearly_commission = JSON.parse(response.yearly_data)
            console.log(yearly_commission)
                // Now prepare the data for the chart
            let months = []
            let commission_made = []
            let commission_colors = []
                //now iterate the sales data and append data to the arrays
            for (const month of yearly_commission) {
                months.push(month.month);
                commission_made.push(month.amount);
                commission_colors.push('rgba(99, 255, 132, 1)');
            }
            //now draw the chart
            var ctx = document.getElementById('yearly-chart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Commission $',
                        data: commission_made,
                        backgroundColor: commission_colors,
                        borderColor: commission_colors,
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