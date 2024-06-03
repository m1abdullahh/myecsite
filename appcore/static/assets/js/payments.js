fetch("/stripe_config")
.then((result) => { return result.json(); })
.then((data) => {
  const stripe = Stripe(data.public_key);

  document.querySelector("#makePayments").addEventListener("click", (ev) => {
    ev.preventDefault()
    if ($("#checkout-info > div > div > form")[0].checkValidity()) {
        fetch("/create_checkout_session")
    .then((result) => { return result.json(); })
    .then((data) => {
        console.log(data)
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
    } else {
        $("#checkout-info > div > div > form")[0].reportValidity()
    }
  });
});