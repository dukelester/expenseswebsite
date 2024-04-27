
const usernameField = document.querySelector('#usernameField');
const emailField = document.querySelector('#email');
const invalidFeedBackArea = document.querySelector('.invalid_feedback');
const inavlidEmail = document.querySelector('.invalid_feedback_email');

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
            }
        });
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
                inavlidEmail.innerHTML = `<p>${data.email_error}</p>`
            }
        });
    }
});