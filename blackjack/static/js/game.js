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

function PickUpBet() {
    const url = `http://127.0.0.1:8000/api/reduce-balance?id=${userId}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            updateUserBalance();
        }
    };
    xhr.send();
}

function MakeBet() {
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
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("bet").textContent = `Ставка ${amount}`;
        
        player = data.player_hand;
        dealer = data.dealer_hand;
        
        if (dealer.hidden) {
            document.getElementById("dealer_hand").textContent = `Рука диллера: ? ${dealer.cards[1]}`;
            document.getElementById("dealer_score").textContent = `Очков: одна карта скрыта ${dealer.value}`;
        } else {
            document.getElementById("dealer_hand").textContent = `Рука диллера: ${dealer.cards}`;
            document.getElementById("dealer_score").textContent = `Очков: ${dealer.value}`;
        }


        document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
        document.getElementById("player_score").textContent = `Очков: ${player.value}`;

        document.getElementById('bets_table').style.display = 'none';
        document.getElementById('new_balance').style.display = 'none';
        document.getElementById('stopButton').style.display = 'inline-block';
        document.getElementById('moreButton').style.display = 'inline-block';
        document.getElementById('refundButton').style.display = 'inline-block';
        document.getElementById('doubleButton').style.display = 'inline-block';
        if (amount * 2 > parseFloat(CurrentBalance)) {
            document.getElementById('doubleButton').style.display = 'none';
        }
        PickUpBet();
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

}


function Stop() {
    document.getElementById('stopButton').style.display = 'none';
    document.getElementById('moreButton').style.display = 'none';
    document.getElementById('refundButton').style.display = 'none';
    document.getElementById('doubleButton').style.display = 'none';
}


function Refund() {
    const url = `http://127.0.0.1:8000/api/refund?id=${userId}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        updateUserBalance();
        document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
        document.getElementById("player_score").textContent = `Очков: ${player.value}. Вы отказались от карт и получили назад половину ставки.`;
        document.getElementById('stopButton').style.display = 'none';
        document.getElementById('moreButton').style.display = 'none';
        document.getElementById('refundButton').style.display = 'none';
        document.getElementById('doubleButton').style.display = 'none';
        document.getElementById('restartButton').style.display = 'inline-block';

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function More() {
    const url = `http://127.0.0.1:8000/api/player-turn?id=${userId}&turn=more`;
    fetch(url)
    .then(response => response.json())
    .then(data => {        
        player = data.player_hand;

        if (player.value <= 21) {
            document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}`;
            document.getElementById('stopButton').style.display = 'inline-block';
            document.getElementById('moreButton').style.display = 'inline-block';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
        } else {
            Lose();
            document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}. Вы перебрали и проиграли.`;
            document.getElementById('stopButton').style.display = 'none';
            document.getElementById('moreButton').style.display = 'none';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
            document.getElementById('restartButton').style.display = 'inline-block';
        }

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}


function Lose() {
    const url = `http://127.0.0.1:8000/api/lose?id=${userId}`;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            updateUserBalance();
        }
    };
    xhr.send();
}




function Double() {
    const url = `http://127.0.0.1:8000/api/player-turn?id=${userId}&turn=double`;
    PickUpBet();
    fetch(url)
    .then(response => response.json())
    .then(data => {        
        player = data.player_hand;

        if (player.value <= 21) {
            document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}`;
            document.getElementById('stopButton').style.display = 'none';
            document.getElementById('moreButton').style.display = 'none';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
        } else {
            Lose();
            document.getElementById("player_hand").textContent = `Ваша рука: ${player.cards}`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}. Вы перебрали и проиграли двойную ставку.`;
            document.getElementById('stopButton').style.display = 'none';
            document.getElementById('moreButton').style.display = 'none';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
            document.getElementById('restartButton').style.display = 'inline-block';
        }

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}


function Restart() {
    document.getElementById('bets_table').style.display = 'block';
    document.getElementById("bet").textContent = `Ставкок нет`;
    document.getElementById("dealer_hand").textContent = `Рука диллера: ? ?`;
    document.getElementById("dealer_score").textContent = `Очков: ?`;
    document.getElementById("player_hand").textContent = `Ваша рука: ? ?`;
    document.getElementById("player_score").textContent = `Очков: ?`;
    document.getElementById('restartButton').style.display = 'none';
    document.getElementById('new_balance').style.display = 'block';
}






updateUserBalance();
