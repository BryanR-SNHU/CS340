document.getElementById('getStockForm').addEventListener('submit', function(s) {
    s.preventDefault();
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/getStock/" + this.elements["stockname"].value;
}, true);

document.getElementById('getIndustryForm').addEventListener('submit', function(s) {
    s.preventDefault();
    window.location.href = "http://127.0.0.1:8080/stocks/api/v1.0/getIndustry/" + this.elements["industry"].value;
}, true);