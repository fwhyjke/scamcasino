// Получаем ссылки на элементы
var modal = document.getElementById("myModal");
var btn = document.getElementById("startGameBtn");
var span = document.getElementsByClassName("close")[0];

// При нажатии кнопки "Начать игру" показываем модальное окно и скрываем кнопку
btn.onclick = function () {
    modal.style.display = "block";
    btn.style.display = "none"; // Скрытие кнопки
}

// При клике на крестик закрываем модальное окно и отображаем кнопку
span.onclick = function () {
    modal.style.display = "none";
    btn.style.display = "block"; // Отображение кнопки
}

// При клике вне модального окна закрываем его и отображаем кнопку
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        btn.style.display = "block"; // Отображение кнопки
    }
}
