const passwordInput = document.getElementById('form-pass')

document.getElementById('btn-login').onclick = async () => {
    password = await eel.generate_password()();
    passwordInput.value = await navigator.clipboard.readText();
    if (passwordInput.value == password) {
        window.location.href = 'index.html'
    }
}

//document.getElementById('btn-paste').onclick = async () => {
//    passwordInput.value = await navigator.clipboard.readText();
//}
