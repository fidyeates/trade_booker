
function on_currency_changed () {
    /*
    Called when either of the dropdown or sell currency box is changed, allows for a more responsive feel to the UI
     */
    let sellCurrency = $("#sell_currency").children("option:selected").val();
    let buyCurrency = $("#buy_currency").children("option:selected").val();
    if ((sellCurrency) && (buyCurrency)) {
        calculate_rate(sellCurrency, buyCurrency);
    }
}


function calculate_rate(sellCurrency, buyCurrency) {
    /*
    Calls a the remote fixer.io api endpoint to get the latest rate and performs the conversion
     */
    let amount = $("#sell_amount").val();

    // Perform an ajax get request to the currency exchange website.
    let post_data = {
        from: sellCurrency,
        to: buyCurrency
    };
    $.ajax({
        type: "POST",
        url: "/rates",
        data: JSON.stringify(post_data),
        success: function(data, status) {
            if (data.success) {
                let rate = data.rate;
                let result = rate * amount;
                $("#rate").attr("placeholder", rate.toFixed(4));
                $("#buy_amount").attr("placeholder", result.toFixed(2));
                $("#submit").attr("disabled", false)
            } else {
                alert("Error saving - requires better error handling in the frontend")
            }
        },
        error: function(data, status) {
            // Should have better error handling from frontend issues, propogating to a backend error handling
            // and logging system
            console.log("Error:", data, status);
        },
        dataType: "json"
    });
}


function submit_trade() {
    // Post the trade back to the web-application
    let post_data = {
        sell_currency: $("#sell_currency").children("option:selected").val(),
        buy_currency: $("#buy_currency").children("option:selected").val(),
        sell_amount: $("#sell_amount").val(),
        buy_amount: $("#buy_amount").attr("placeholder"),
        rate: $("#rate").attr("placeholder"),
    }
    $.ajax({
        type: "POST",
        url: "/book",
        data: JSON.stringify(post_data),
        success: function(data, status) {
            if (data.success) {
                window.location = "/";
            } else {
                alert("Error saving - requires better error handling in the frontend")
            }
        },
        error: function(data, status) {
            // Should have better error handling from frontend issues, propogating to a backend error handling
            // and logging system
            console.log("Error:", data, status);
        },
        dataType: "json"
    });
}

function cancel_booking() {
    window.location = "/";
}
