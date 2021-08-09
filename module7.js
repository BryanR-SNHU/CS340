// Append the provided stock to the end of the getStock endpoint URL.
document.getElementById('getStockForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/getStock/" + this.elements["stockname"].value;
}, true);

// Append the provided industry to the end of the getIndustry enpoint URL.
document.getElementById('getIndustryForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/getIndustry/" + this.elements["industry"].value;
}, true);

// POST the provided high and low values to the getAverage endpoint.
document.getElementById('getAverageForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    var postRequest = new XMLHttpRequest;
    postRequest.onload = function(r) // Function to display results.
    {
        document.getElementById('averageResult').innerText = postRequest.responseText; // Will get executed asynchronously when the response arrives.
    }
    postRequest.open("POST", "/stocks/api/v1.0/getAverage", true)
    postRequest.setRequestHeader('Content-Type', 'application/json');
    postRequest.send(JSON.stringify({low: this.elements["low"].value, high: this.elements["high"].value})); // Format the form values into JSON.
}, true);

// Append the provided industry to the industryReport endpoint URL.
document.getElementById('getIndustryReportForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/industryReport/" + this.elements["industry"].value;
}, true);

// Append the provided company name to the portfolio endpoint URL.
document.getElementById('getPortfolioForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/portfolio/" + this.elements["company"].value;
}, true);

// POST the provided stock names to the stockReport endpoint.
document.getElementById('getStockReportForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    
    stockString = this.elements["stockArr"].value;
    stockArr = stockString.split(',');

    var postRequest = new XMLHttpRequest;
    postRequest.onload = function(r) // Function to display results.
    {
        document.getElementById('reportResult').innerText = postRequest.responseText; // Will get executed asynchronously when the response arrives.
    }
    postRequest.open("POST", "/stocks/api/v1.0/stockReport", true)
    postRequest.setRequestHeader('Content-Type', 'application/json');
    postRequest.send(JSON.stringify(stockArr));
}, true);

// PUT the provided volume at an enpoint determined by the provided stock name.
document.getElementById('updateStockForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.
    var putRequest = new XMLHttpRequest;
    putRequest.onload = function(r) // Function to display results.
    {
        document.getElementById('updateResult').innerText = putRequest.responseText; // Will get executed asynchronously when the response arrives.
    }
    putRequest.open("PUT", "/stocks/api/v1.0/updateStock/" + this.elements["stockname"].value, true) // Use the stock name from the form to select the right endpoint.
    putRequest.setRequestHeader('Content-Type', 'application/json');
    putRequest.send(JSON.stringify({Volume: this.elements["volume"].value})); // PUT the "volume" value at the endpoint.
}, true);

// Append the provided stock name to the deleteStock URL.
document.getElementById('deleteStockForm').addEventListener('submit', function(s) {
    s.preventDefault(); // Prevents the form from being submitted.

    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/deleteStock/" + this.elements["stockname"].value;
}, true);