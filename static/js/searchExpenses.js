const searchField = document.querySelector('#searchField');
const outputTable = document.querySelector('.output');
outputTable.style.display = 'none'

const expensesTable = document.querySelector('.expensesTable');
const pagination = document.querySelector('.pagination-container');

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim()) {
        pagination.style.display = 'none';
        fetch('/search_expense', {body: JSON.stringify({searchText: searchValue})
        , method: "POST"
    }).then((res) => res.json()).then((data) => {
        expensesTable.style.display = 'none';
        if (data.length === 0){
            outputTable.innerHTML = '<p> There is no results for you!</p>'
        } else {
            outputTable.style.display = 'block';
            
        }
    });
    }
});