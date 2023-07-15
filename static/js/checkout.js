var form = document.getElementById('form')
var submitBtn = document.getElementById('submit-btn')
var paymentInfo = document.getElementById('payment-info')
var payBtn = document.getElementById('make-payment')
var userInfo = document.getElementById('user-info')

if (user != 'AnonymousUser' && userInfo != null ) {
    userInfo.innerHTML = ''
}

if (form != null) {
    form.addEventListener('submit', function(e){
        e.preventDefault()
        console.log('submited')
        submitBtn.classList.add('hidden')
        paymentInfo.classList.remove('hidden')
    })


    payBtn.addEventListener('click', (e)=>{
        submitForm()
    })

    function submitForm(e){
        console.log('Payment successful!');
        alert('Payment successful!')
    }
}
