fetch("/conf/")
    .then((result) => {
        return result.json();
    })
    .then((data) => {
        // Initialize Stripe.js
        // noinspection JSUnresolvedFunction
        const stripe = Stripe(data.publicKey);
        document.querySelector("#submitBtn").addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/new/")
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    // Redirect to Stripe Checkout
                    // noinspection JSUnresolvedFunction
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
        });
    });
