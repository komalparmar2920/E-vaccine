function onChange() {
    const password = document.querySelector('input[name=password]');
    const confirm = document.querySelector('input[name="conf_password"]');
    const email = document.querySelector('input[name="email"]')
    if (confirm.value == password.value) 
    {
        confirm.setCustomValidity('');
    } else {
      confirm.setCustomValidity('Passwords does not match');
    }

    
}




  