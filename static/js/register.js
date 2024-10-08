
const usernameField = document.querySelector('#usernameField');
const emailField = document.querySelector('#email');
const invalidFeedBackArea = document.querySelector('.invalid_feedback');
const inavlidEmail = document.querySelector('.invalid_feedback_email');
const passwordField = document.querySelector('.password');
const confirmPasswordField = document.querySelector('#password2');
const showAPasswordToggle = document.querySelector('#showAPasswordToggle');

const accountButton = document.querySelector('.account-btn');

showAPasswordToggle.addEventListener('click', (e) => {
    if (showAPasswordToggle.textContent === 'SHOW') {
        showAPasswordToggle.textContent = 'HIDE';
        passwordField.setAttribute('type', 'text');
        confirmPasswordField.setAttribute('type', 'text');
    } else {
        showAPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute('type', 'password');
        confirmPasswordField.setAttribute('type', 'password');
    };
});


usernameField.classList.remove('is-invalid');
invalidFeedBackArea.style.display = 'none';
emailField.classList.remove('is-invalid');
inavlidEmail.style.display = 'none';
// add eventy listener - keyup
usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;
    // console.log(usernameValue);
    if (usernameValue) {
        fetch('/authentication/validate_username', {
            body: JSON.stringify({ username: usernameValue }), method: 'POST'
        }).then(res => res.json()).then(data => {
            // console.log(data);
            if (data.username_error){
                usernameField.classList.add('is-invalid');
                invalidFeedBackArea.style.display = 'block';
                invalidFeedBackArea.innerHTML = `<p>${data.username_error}</p>`
                accountButton.disabled = true;
            } else {
                accountButton.disabled = false;
            }
        });
    } else {
        accountButton.disabled = true;
    }
});

// add eventy listener - keyup on the email
emailField.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;
    console.log(emailValue);
    if (emailValue) {
        fetch('/authentication/validate_email',{
            body: JSON.stringify({ email: emailValue }), method: 'POST'
        }).then(res => res.json()).then(data => {
            console.log(data);
            if(data.email_error) {
                emailField.classList.add('is-invalid');
                inavlidEmail.style.display = 'block';
                inavlidEmail.innerHTML = `<p>${data.email_error}</p>`;
                accountButton.disabled = true;
            } else {
                accountButton.disabled = false;
            }
        });
    } else {
        accountButton.disabled = true;
    }
});