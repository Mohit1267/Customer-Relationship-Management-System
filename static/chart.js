const quarterlyChart = new Chart(document.getElementById('quarterlyChart'), {
    type: 'pie',  // Chart type
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],  // Labels for each segment
        datasets: [{
            label: 'Quarterly Data',
            data: [20, 10, 30, 40],  // Data for each segment
            backgroundColor: [ // Custom colors for each segment
                'rgba(255, 99, 132, 0.8)',  // Color for Q1
                'rgba(54, 162, 235, 0.8)',  // Color for Q2
                'rgba(255,206, 86, 0.8)',  // Color for Q3
                'rgba(75, 192, 192, 0.8)'   // Color for Q4
            ],
            borderColor: [ // Border colors for each segment
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1 // Width of the border
        }]
    },
    options: {
        plugins: {
            legend: {
                labels: {
                    color: 'white' // Legend text color
                }
            },
            tooltip: {
                titleColor: 'white', // Tooltip title color
                bodyColor: 'white',  // Tooltip body color
                backgroundColor: '#007d7e' // Tooltip background color
            }
        }
    }
});

