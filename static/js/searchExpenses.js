const searchField = document.querySelector('#searchField');
const outputTable = document.querySelector('.output');
outputTable.style.display = 'none'

const expensesTable = document.querySelector('.expensesTable');
const pagination = document.querySelector('.pagination-container');

const tableBody = document.querySelector('.tbody');

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim()) {
        pagination.style.display = 'none';
        tableBody.innerHTML = '';
        fetch('/search_expense', {body: JSON.stringify({searchText: searchValue})
        , method: "POST"
    }).then((res) => res.json()).then((data) => {
        expensesTable.style.display = 'none';
        if (data.length === 0){
            outputTable.innerHTML = '<p> There is no results for you!</p>'
        } else {
            console.log(data, data.length)
            outputTable.style.display = 'block';
            data.forEach(element => {
                tableBody.innerHTML += `
                <td>${ element.id }</td>
                <td>${ element.amount }</td>
                <td>${ element.category }</td>
                <td>${ element.description }</td>
                <td> ${ element.date }</td>
                `
            });
            
        }
    });
    } else {
        outputTable.style.display = 'none';
        pagination.style.display = 'block';
        expensesTable.style.display = 'block';
    }
});