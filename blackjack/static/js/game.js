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

function resetBalance() {
    const url = `http://127.0.0.1:8000/api/reset-balance?id=${userId}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log('Запрос успешно отправлен!');
            updateUserBalance();
        }
    };
    xhr.send();
}
