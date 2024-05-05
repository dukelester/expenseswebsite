const ctx = document.getElementById('myChart');

const renderChart = (data, labels) => {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            label: 'Last Six Months Expenses',
            data: data,
            borderWidth: 1
          }]
        },
        options: {
          title: {
              display: true,
              text: "Expenses per Category"
          }
        }
      });
}


const getChartData = () => {
    fetch('/expenses_category_summary')
    .then((res) => res.json())
    .then((results) => {
        console.log(results);
        const categoryData = results.expense_category_data;
        console.log(categoryData)
        const [labels, data] = [Object.keys(categoryData), Object.values(categoryData)];
        renderChart(data, labels);
    });
};
document.onload = getChartData()