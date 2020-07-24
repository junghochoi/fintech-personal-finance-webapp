$.ajax({
    url: "/analysis/balance"
}).done((data)=>{
    
    
    let transactions = data['data'];
    let dates = transactions.map(t => t.date);
    let names = transactions.map(t => t.name)
    let balances = transactions.map(b => b.result);

    userData =  {
        labels: names,
        datasets: [{
            label: 'Balance',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: balances
        }]
    };

    config = {
        responsive: true,
        tooltips: {
            enabled: true,
            mode: 'single',
            callbacks:{
                title: function(tooltipItems, data){
                    return 'Name: ' + names[tooltipItems[0].index] + '\nDate: ' + dates[tooltipItems[0].index];
                }
            }
        }

    }


    let ctx = document.getElementById('income-chart').getContext('2d');
    let chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',
        // The data for our dataset
        data: userData,
        // Configuration options go here
        options: config
    });




    // Create more buttons to filter out by Week,Month,Year,All
    $('#update').on('click', ()=>{
        userData.datasets[0].data[0]= 100;
        chart.update()
    });
});


$.ajax({
    url: '/analysis/categories'
}).done((res)=>{
    

    categories = Object.keys(res)
    expenses = Object.values(res);
    barData = {
        labels: categories,
        datasets:[{
            label: 'Amount Spent',
            data: expenses,


            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    };


    barOptions = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

    pieData = {
        labels: categories,
        datasets: [{
            data: expenses,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
        }]
    }

    pieOptions = {
        animation: {
            animateRotate: true,
            animateScale: true

        }
    }
    let barCanvas = document.getElementById('categories-barchart').getContext('2d');
    let categoriesBarChart = new Chart(barCanvas,{
        type: 'horizontalBar',
        data: barData,
        options: barOptions

    });

    let pieCanvas = document.getElementById('categories-piechart').getContext('2d');
    let categoriesPieChart = new Chart(pieCanvas,{
        type: 'pie',
        data: pieData,
        options: pieOptions
    });
});
