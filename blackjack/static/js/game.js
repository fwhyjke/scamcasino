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

function resetBalance() {
    const url = `http://127.0.0.1:8000/api/reset-balance?id=${userId}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            updateUserBalance();
        }
    };
    xhr.send();
}

function Bet() {
    const amount = document.getElementById("balanceInput").value;
    const url = `http://127.0.0.1:8000/api/start-game?id=${userId}&bet=${amount}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // После успешного завершения запроса на сброс баланса вызываем updateUserBalance()
            updateUserBalance();
        }
    };
    xhr.send();
}

updateUserBalance();
