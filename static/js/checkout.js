var form = document.getElementById('form')
var submitBtn = document.getElementById('submit-btn')
var paymentInfo = document.getElementById('payment-info')
var payBtn = document.getElementById('make-payment')
var userInfo = document.getElementById('user-info')
var total = '{{order.get_total|floatformat:2}}'

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

        var userForm = {
            'name':null,
            'email':null,
            'total':total,
        }

        var shippingInfo = {
            'address': null,
            'city': null,
            'postcode': null,
        }

        if (user == 'AnonymousUser'){
            userForm.name = form.name.value
            userForm.email = form.email.value
        }

        shippingInfo.address = form.address.value
        shippingInfo.city = form.city.value
        shippingInfo.postcode = form.postcode.value

        console.log('User Info: ', userForm);
        console.log('Shipping Info: ', shippingInfo);
    }
}
