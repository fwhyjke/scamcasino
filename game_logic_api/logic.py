import random


# Основной файл, где и описана логика расчета игры


# Класс для колоды карт
class Deck:
    # При инициализации передается уже сущетвующая колода, либо пустой список. Если пустой список - создается новая
    # колода из 4 колод по 52 карты. Если колода уже есть - игра продолжается с ней же.
    def __init__(self, deck):
        if len(deck) < 104:
            self.deck = []
            cards = ['2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', 'Jc', 'Qc', 'Kc', 'Ac',
                     '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', 'Jd', 'Qd', 'Kd', 'Ad',
                     '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', 'Jh', 'Qh', 'Kh', 'Ah',
                     '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'Js', 'Qs', 'Ks', 'As']
            self.deck = cards * 4
        else:
            self.deck = deck

    # Статический метод для определений стоимости карты.
    @staticmethod
    def get_nominal(card):
        # Если перебора нет - туз равен 11, а если есть - он помечается и будет расцениваться как 1. Помечать нужно на
        # случай выподания нескольких тузов в колоде.
        nominals = {
            'A1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 10,
            'Q': 10,
            'K': 10,
            'A': 11
        }
        return nominals[card[:-1]]  # При поиске номинала, масть не имеет значения.

    # Метод для перетосовки колоды
    def shuffle_deck(self):
        random.shuffle(self.deck)

    # Метод, который выдает новую карту из колоды в виде списка из её названия и номинала.
    def take_card(self):
        card = self.deck.pop()
        return [card, self.get_nominal(card)]


# Класс отвечающий за реализацию набора карт. Подходит как для диллера, так и для игрока.
class Hand:
    # При инициализации важно понимать, скрыта ли одна из карт или нет. Это необходимо для диллера.
    def __init__(self, cards, value, hidden=False):
        if not hidden:
            self.hidden = hidden
            # Если при инициализации было указано -1, то создается пустая рука, ещё без карт. Иначе используются ранее
            # полученные карты
            if cards == -1:
                self.cards = []
                self.value = 0
            else:
                self.cards = cards
                self.value = value
        else:
            self.hidden = hidden
            if cards == -1:
                self.cards = []
                self.value = 0
            else:
                self.cards = cards
                self.value = value - cards[0]

    # Метод, отвечающий за получение новой карты на руки. Напомню, что карта представляет собой список [Масть, номинал]
    def add_card(self, card):
        # Добавляем в список имеющихся карт карту и увеличиваем общий счет
        self.cards.append(card[0])
        self.value += card[1]
        # Если видим перебор, то проверяем, есть ли у нас тузы
        if self.value > 21 and any([i in self.cards for i in ['Ac', 'Ad', 'Ah', 'As']]):
            # Если есть, тогда находим все тузы на руке
            count_A = [i for i in self.cards if i in ['Ac', 'Ad', 'Ah', 'As']]
            # И пока перебор не исчезнет, меняем номинал туза на однерку по очереди
            while len(count_A) != 0 and self.value > 21:
                self.value -= 10
                A = count_A.pop()
                del self.cards[self.cards.index(A)]
                self.cards.append(f'A1{A[-1]}')

    # Метод для удобного представления карты
    def __str__(self):
        return f'{self.cards}'
