function updateUserBalance() {
    const url = `http://127.0.0.1:8000/api/user-balance?id=${userId}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("balance").textContent = `Balance: ${data}`;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}
updateUserBalance();

setInterval(updateUserBalance, 2000);
