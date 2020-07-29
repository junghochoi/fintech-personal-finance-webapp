console.log("connected")

balancesChartSetup = (transactions) =>{
    let dates = transactions.map(t => t.date);
    let names = transactions.map(t => t.title)
    let balances = transactions.map(t => t.result);
    let notes = transactions.map(t => t.notes);
    let change = transactions.map(t=> t.amount);
    let types = transactions.map(t=>t.main_category);
    let categories = transactions.map(t=>t.spec_category);

    userData =  {
        labels: dates,
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
            titleFontSize: 14,
            titleSpacing: 4,
            enabled: true,
            mode: 'single',
            callbacks:{
                title: function(tooltipItems, data){

                    return `Name: ${names[tooltipItems[0].index]}\nChange: ${change[tooltipItems[0].index]}\nDate: ${dates[tooltipItems[0].index]}\nCategory: ${categories[tooltipItems[0].index]}\nNotes: ${notes[tooltipItems[0].index]}`
           
                }
            }
        },
        elements: {
            line: {
                tension: 0
            }
        },
        pointHitRadius: 5,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
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
}

categoriesChartSetup = (data) =>{
    
    console.log(data)
    categories = Object.keys(data)
    expenses = Object.values(data);
    barData = {
        labels: categories,
        datasets:[{
            
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
        title:{
            display: true,
            text: 'Total Expenses'
        },
        scales: {
            xAxes: [{
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
}

incomeExpenseChartSetup = (data)=> {


    categories = Object.keys(data)
    numbers = Object.values(data);
    

    barData = {
        labels: categories,
        datasets:[{
            
            data: numbers,


            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',

            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',

            ],
            borderWidth: 3
        }]
    };


    barOptions = {
        title:{
            display: true,
            text: 'Income vs Expense'
        },
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };


    let barCanvas = document.getElementById('income-expense-chart').getContext('2d');
    let categoriesBarChart = new Chart(barCanvas,{
        type: 'horizontalBar',
        data: barData,
        options: barOptions

    });
}

$.ajax({
    url: "/analysis/total"
}).done((data)=>{
    
    let transactions = data['balance'];
    let categories = data['categories']
    let incomeExpense = data['income-expense']

    balancesChartSetup(transactions);
    categoriesChartSetup(categories);
    incomeExpenseChartSetup(incomeExpense);
});

