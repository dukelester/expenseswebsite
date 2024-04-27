
const usernameField = document.querySelector('#usernameField');

// add eventy listener - keyup
usernameField.addEventListener('keyup', (e) => {
    usernameValue = e.target.value;
    console.log(usernameValue);
    if (usernameValue) {
        fetch('/authentication/validate_username', {
            body: JSON.stringify({ username: usernameValue }), method: 'POST'
        }).then(res => res.json()).then(data => {
            console.log(data);
        });
    }
});
