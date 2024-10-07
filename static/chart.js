const quarterlyChart = new Chart(document.getElementById('quarterlyChart'), {
    type: 'pie',  // Chart type
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
            label: 'Quarterly Data',
            data: [20, 10, 30, 40],
            backgroundColor: [

            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
                '#990000',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: 'red'
                }
            },
            tooltip: {
                titleColor: '#990000',
                bodyColor: 'white',
                backgroundColor: '#007d7e'
            }
        }
    }
});

