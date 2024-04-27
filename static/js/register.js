
const usernameField = document.querySelector('#usernameField');
const invalidFeedBackArea = document.querySelector('.invalid_feedback');
usernameField.classList.remove('is-invalid');
invalidFeedBackArea.style.display = 'none';
// add eventy listener - keyup
usernameField.addEventListener('keyup', (e) => {
    usernameValue = e.target.value;
    console.log(usernameValue);
    if (usernameValue) {
        fetch('/authentication/validate_username', {
            body: JSON.stringify({ username: usernameValue }), method: 'POST'
        }).then(res => res.json()).then(data => {
            console.log(data);
            if (data.username_error){
                usernameField.classList.add('is-invalid');
                invalidFeedBackArea.style.display = 'block';
                invalidFeedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }
        });
    }
});
