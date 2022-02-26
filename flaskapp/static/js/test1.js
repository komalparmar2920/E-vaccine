function onClick()
{
    const email = document.querySelector('input[name=email]');
    const password = document.querySelector('input[name=pass]');
    if(email.value == test(form1.email.value))
    {
        confirm.setCustomValidity('');
        return (true)
    }
    else{
        confirm.setCustomValidity('Please enter valied email_id');
        return (False)
    }

    
}