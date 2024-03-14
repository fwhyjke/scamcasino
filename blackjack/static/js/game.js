var CurrentBalance = 0

function updateUserBalance() {
    const url = `http://127.0.0.1:8000/api/user-balance?id=${userId}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            CurrentBalance = data
            document.getElementById("balance").textContent = `Balance: ${CurrentBalance}`;
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

    if (amount < 0) {
        alert("Пожалуйста, введите корректную сумму ставки. Ставка не может быть отрицательной!");
        return;
    }
    if (amount > parseFloat(CurrentBalance)) {
        alert("Недостаточно средств на счету! Пожалуйста, введите корректную сумму ставки.");
        return;
    }
    

    const url = `http://127.0.0.1:8000/api/start-game?id=${userId}&bet=${amount}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            updateUserBalance();
        }
    };
    xhr.send();
}

updateUserBalance();
