const searchField = document.querySelector('#searchField');

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue.trim()) {
        fetch('/search_expense', {body: JSON.stringify({searchText: searchValue})
        , method: "POST"
    }).then((res) => res.json()).then((data) => {
        console.log(data);
    });
    }
});