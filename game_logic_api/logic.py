# Основной файл, где и описана логика расчета игры

import random


class Deck:
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

    @staticmethod
    def get_nominal(card):
        nominals = {
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
        return nominals[card[:-1]]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def take_card(self):
        card = self.deck.pop()
        return [card, self.get_nominal(card)]


class Hand:
    def __init__(self, cards, value, hidden=False):
        if not hidden:
            self.hidden = hidden
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

    def add_card(self, card):
        self.cards.append(card[0])
        self.value += card[1]

    def __str__(self):
        return f'{self.cards}'


def determine_winner(player_hand, dealer_hand, status) -> float:
    if status == 'refund':
        return 0.5

    elif status == 'more':
        if player_hand > 21:
            return 0
        else:
            return 200

    elif status == 'stop':
        if player_hand > 21:
            return 0
        elif dealer_hand.value > 21:
            return 2
        elif player_hand.value == dealer_hand:
            return 1
        elif player_hand.value > dealer_hand:
            return 2

    elif status == 'double':
        if player_hand > 21:
            return -1
        elif dealer_hand.value > 21:
            return 3
        elif player_hand.value == dealer_hand:
            return 1
        elif player_hand.value > dealer_hand:
            return 3
