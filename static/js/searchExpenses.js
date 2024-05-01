const searchField = document.querySelector('#searchField');

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;
    if (searchValue) {
        console.log(searchValue);
    }
});