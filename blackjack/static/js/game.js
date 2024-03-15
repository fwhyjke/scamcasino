var CurrentBalance = 0

function updateUserBalance() {
    const url = `http://127.0.0.1:8000/api/user-balance?id=${userId}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            CurrentBalance = data
            document.getElementById("balance").textContent = `${CurrentBalance.bal}`;
            document.getElementById("rec").textContent = `${CurrentBalance.rec}`;
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

    if (amount.trim() === "") {
        alert("Пожалуйста, введите сумму ставки.");
        return;
    }
    if (amount < 0) {
        alert("Пожалуйста, введите корректную сумму ставки. Ставка не может быть отрицательной!");
        return;
    }
    if (amount > parseFloat(CurrentBalance)) {
        alert("Недостаточно средств на счету! Пожалуйста, введите корректную сумму ставки.");
        return;
    }
    document.getElementById("bet").style.display = 'block';
    document.getElementById("dealer_hand").style.display = 'block';
    document.getElementById("1").style.display = 'block';
    document.getElementById("2").style.display = 'block';
    document.getElementById("dealer_score").style.display = 'block';
    document.getElementById("player_hand").style.display = 'block';
    document.getElementById("player_score").style.display = 'block';
    document.getElementById('new_balance').style.display = 'block';
    document.getElementById('result').style.display = 'none';
    const url = `http://127.0.0.1:8000/api/start-game?id=${userId}&bet=${amount}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        document.getElementById("bet").textContent = `Ставка: ${amount}`;
        
        player = data.player_hand;
        dealer = data.dealer_hand;
        
        if (dealer.hidden) {
            document.getElementById("dealer_hand").innerHTML = `<img class="card_img" src="static/images/back.png" alt="Скрытая карта"> <img class="card_img" src="static/images/${dealer.cards[1]}.png" alt="${dealer.cards[1]}">`;
            document.getElementById("dealer_score").textContent = `Очков: карта скрыта`;
        } else {
            document.getElementById("dealer_hand").innerHTML = `<img class="card_img" src="static/images/${dealer.cards[0]}.png" alt="${dealer.cards[0]}"> <img class="card_img" src="static/images/${dealer.cards[1]}.png" alt="${dealer.cards[1]}">`;
            document.getElementById("dealer_score").textContent = `Очков: ${dealer.value}`;
        }

        document.getElementById("player_hand").innerHTML = `<img class="card_img" src="static/images/${player.cards[0]}.png" alt="${player.cards[0]}"> <img class="card_img" src="static/images/${player.cards[1]}.png" alt="${player.cards[1]}">`;
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
        if (player.value === 21) {
            GameResult();
            document.getElementById('stopButton').style.display = 'none';
            document.getElementById('moreButton').style.display = 'none';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
        }
        document.getElementById('game').style.display = 'flex';

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

}


function Stop() {
    const url = `http://127.0.0.1:8000/api/stop?id=${userId}`;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
    document.getElementById('stopButton').style.display = 'none';
    document.getElementById('moreButton').style.display = 'none';
    document.getElementById('refundButton').style.display = 'none';
    document.getElementById('doubleButton').style.display = 'none';
    DealerTurn();
}


function Refund() {
    const url = `http://127.0.0.1:8000/api/refund?id=${userId}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        updateUserBalance();
        document.getElementById("player_hand").innerHTML = `<img class="card_img" src="static/images/${player.cards[0]}.png" alt="${player.cards[0]}"> <img class="card_img" src="static/images/${player.cards[1]}.png" alt="${player.cards[1]}">`;
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
            var handHtml = "";
            for (var i = 0; i < player.cards.length; i++) {
                handHtml += `<img class="card_img" src="static/images/${player.cards[i]}.png" alt="${player.cards[i]}">`;
            }
            document.getElementById("player_hand").innerHTML = handHtml;

            document.getElementById("player_score").textContent = `Очков: ${player.value}`;
            document.getElementById('stopButton').style.display = 'inline-block';
            document.getElementById('moreButton').style.display = 'inline-block';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
        } else {
            Lose();
            var handHtml = "";
            for (var i = 0; i < player.cards.length; i++) {
                handHtml += `<img class="card_img" src="static/images/${player.cards[i]}.png" alt="${player.cards[i]}">`;
            }
            document.getElementById("player_hand").innerHTML = handHtml;
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
            document.getElementById("player_hand").innerHTML = `<img class="card_img" src="static/images/${player.cards[0]}.png" alt="${player.cards[0]}"> <img class="card_img" src="static/images/${player.cards[1]}.png" alt="${player.cards[1]}"> <img class="card_img" src="static/images/${player.cards[2]}.png" alt="${player.cards[2]}">`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}`;
            document.getElementById('stopButton').style.display = 'none';
            document.getElementById('moreButton').style.display = 'none';
            document.getElementById('refundButton').style.display = 'none';
            document.getElementById('doubleButton').style.display = 'none';
            DealerTurn();
        } else {
            Lose();
            document.getElementById("player_hand").innerHTML = `<img class="card_img" src="static/images/${player.cards[0]}.png" alt="${player.cards[0]}"> <img class="card_img" src="static/images/${player.cards[1]}.png" alt="${player.cards[1]}"> <img class="card_img" src="static/images/${player.cards[2]}.png" alt="${player.cards[2]}">`;
            document.getElementById("player_score").textContent = `Очков: ${player.value}`;
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
    document.getElementById('bets_table').style.display = 'flex';
    document.getElementById("bet").style.display = 'none';
    document.getElementById("dealer_hand").style.display = 'none';
    document.getElementById("1").style.display = 'none';
    document.getElementById("2").style.display = 'none';
    document.getElementById("dealer_score").style.display = 'none';
    document.getElementById("player_hand").style.display = 'none';
    document.getElementById("player_score").style.display = 'none';
    document.getElementById('restartButton').style.display = 'none';
    document.getElementById('new_balance').style.display = 'block';
    document.getElementById('result').style.display = 'none';
}


function DealerTurn() {
    const url = `http://127.0.0.1:8000/api/dealer-turn?id=${userId}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        dealer = data.dealer_hand;

        var handHtml = "";
            for (var i = 0; i < dealer.cards.length; i++) {
                handHtml += `<img class="card_img" src="static/images/${dealer.cards[i]}.png" alt="${dealer.cards[i]}">`;
            }
            document.getElementById("dealer_hand").innerHTML = handHtml;
        document.getElementById("dealer_score").textContent = `Очков: ${dealer.value}`;

        GameResult();

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function GameResult() {
    const url = `http://127.0.0.1:8000/api/result?id=${userId}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        result = data.game;

        if (result === 'win') {
            document.getElementById("result").textContent = `Вы выиграли! Все ваши ставки возвращены в двойном размере!`;
        } else if (result === 'draw') {
            document.getElementById("result").textContent = `Ничья. Все ваши ставки возвращены.`;
        } else if (result === 'lose') {
            document.getElementById("result").textContent = `Вы програли. В следующий раз повезет!`;
        } else if (result === 'blackjack') {
            document.getElementById("result").textContent = `BLACKJACK! Вам сегодня везет! На баланс начислено 3 ваших ставки.`;
        }
        
        document.getElementById('result').style.display = 'block';
        document.getElementById('restartButton').style.display = 'block';
        updateUserBalance();
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

updateUserBalance();
