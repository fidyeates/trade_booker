FIXER_URI = "http://data.fixer.io/api/";
ACCESS_KEY = "edfed567398eaeabd20a295428334ae3";


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
    let URI = "http://data.fixer.io/api/latest?access_key=" + ACCESS_KEY + "&base=" + sellCurrency + "&symbols=" + buyCurrency;

    // Perform an ajax get request to the currency exchange website.
    $.ajax({
        type: "GET",
        url: URI,
        success: function(data, status) {
            let rate = data.rates[buyCurrency];
            let result = rate * amount;
            $("#rate").attr("placeholder", rate.toFixed(4));
            $("#buy_amount").attr("placeholder", result.toFixed(2));
            $("#submit").attr("disabled", false)
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


function setup_symbols() {
    /*
    Gets all available symbols from fixer.io and populates the dropdowns
     */
    let URI = "http://data.fixer.io/api/symbols?access_key=" + ACCESS_KEY;
    $.ajax({
        type: "GET",
        url: URI,
        success: function(data, status) {
            $.each( data.symbols, function( symbol, description ) {
                $("#sell_currency").append(new Option(symbol, symbol));
                $("#buy_currency").append(new Option(symbol, symbol));
            });
        },
        error: function(data, status) {
            // Should have better error handling from frontend issues, propogating to a backend error handling
            // and logging system
            console.log("Error:", data, status);
        },
        dataType: "json"
    });
}