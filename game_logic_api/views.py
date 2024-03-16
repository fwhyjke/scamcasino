import json
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from game_logic_api.models import UserBalance
from game_logic_api.serializers import BalanceSerializer, HandSerializer
from game_logic_api.logic import Deck, Hand
from game_logic_api.utils import delete_session_data


# Главный файл приложения. Здесь реализовано API приложения, которое взаимодействует с JS на стороне клиента.


# Возвращает пользователю его баланс и обновляет рекорд, тк при каждом измениние баланса метод get класса отрабатывает
class GetUserBalanceAPI(APIView):
    def get(self, request):
        # Забираем из запроса id пользователя
        user = request.query_params.get('id')
        # Берем из БД объект его баланса
        balance_object = UserBalance.objects.get(user=user)
        # И преобразуем в словарь
        balance = dict(BalanceSerializer(balance_object).data)
        # Обновляем рекорд
        if balance['balance'] > balance['record']:
            balance_object.record = balance['balance']
            balance_object.save()
            balance['record'] = balance['balanxe']
        # Отдаем данные о балансе и рекорде
        return Response({'bal': balance['balance'], 'rec': balance['record']})


# Реализация обновления баланса. Баланс можно сбросить к начальным 5000.
class ResetBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance = 5000
        balance_object.save()
        return Response({"message": "Баланс успешно сброшен"})


# Реализация начала игры
class StartGameAPI(APIView):
    def get(self, request):
        # берем из запроса пользователя и ставку
        user = request.query_params.get('id')
        bet = request.query_params.get('bet')
        cards = Deck([])
        # перемешиваем колоду
        cards.shuffle_deck()
        # Создаем два объекта для руки диллера и игрока
        player_hand = Hand(-1, -1)
        dealer_hand = Hand(-1, -1, hidden=True)
        # Раздаем карты
        for _ in range(2):
            player_hand.add_card(cards.take_card())
            dealer_hand.add_card(cards.take_card())

        # Переводим в формат для отправки в ответ
        player_hand_serializer = HandSerializer(player_hand)
        dealer_hand_serializer = HandSerializer(dealer_hand)

        # Если выпало сразу 21 (Туз и картинка / 10), то пользователь автоматически побеждает
        if player_hand.value == 21:
            response_data = {
                "player_hand": player_hand_serializer.data,
                "dealer_hand": dealer_hand_serializer.data,
                "blackjack": 1
            }
            # Заносим в редис пару ключ - значение, где значение - то, с каким статусом прошла игра
            redis_conn = get_redis_connection("default")
            redis_conn.set(f'user_{user}_status', 'blackjack')
        else:
            response_data = {
                "player_hand": player_hand_serializer.data,
                "dealer_hand": dealer_hand_serializer.data,
                "blackjack": 0
            }

        # Заносим в редис все данные о начавшейся игре
        redis_conn = get_redis_connection("default")
        redis_conn.set(f'user_{user}_bet', bet)
        redis_conn.set(f'user_{user}_player_hand', json.dumps(player_hand_serializer.data))
        redis_conn.set(f'user_{user}_dealer_hand', json.dumps(dealer_hand_serializer.data))
        redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))

        return Response(response_data)


# Класс, отвечающий за ход игрока
class PlayerTurnAPI(APIView):
    def get(self, request):
        # берем id пользователя и то, какой он ход выбрал из запроса.
        user = request.query_params.get('id')
        turn = request.query_params.get('turn')
        # если выбрал ещё - добавляем ещё карты, попутно обновляе данные о игре в redis, после чего отправляем
        # результаты на клинет
        if turn == 'more':
            redis_conn = get_redis_connection("default")
            redis_conn.set(f'user_{user}_status', 'more')
            cards = json.loads(redis_conn.get(f'user_{user}_cards_deck').decode('utf-8').replace("'", '"'))
            cards = Deck(cards)
            player_hand = json.loads(redis_conn.get(f'user_{user}_player_hand').decode('utf-8'))
            player_hand = Hand(player_hand['cards'], player_hand['value'])
            player_hand.add_card(cards.take_card())
            player_hand_serializer = HandSerializer(player_hand)
            response_data = {
                "player_hand": player_hand_serializer.data,
            }

            redis_conn.set(f'user_{user}_player_hand', json.dumps(player_hand_serializer.data))
            redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))

            return Response(response_data)
        if turn == 'double':
            # сценарий, если игрок решил удвоить. Берется ещё одна карта, ставка повторно списывается с баланса,
            # и отправляется результат на клиент, где будут убраны все кнопки, пока диллер не возьмет карты
            redis_conn = get_redis_connection("default")
            redis_conn.set(f'user_{user}_status', 'double')
            cards = json.loads(redis_conn.get(f'user_{user}_cards_deck').decode('utf-8').replace("'", '"'))
            cards = Deck(cards)
            player_hand = json.loads(redis_conn.get(f'user_{user}_player_hand').decode('utf-8'))
            player_hand = Hand(player_hand['cards'], player_hand['value'])
            player_hand.add_card(cards.take_card())
            player_hand_serializer = HandSerializer(player_hand)
            response_data = {
                "player_hand": player_hand_serializer.data,
            }

            redis_conn.set(f'user_{user}_player_hand', json.dumps(player_hand_serializer.data))
            redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))

            return Response(response_data)


# Если игрок програл, то отправляем соответствующее сообщение и удаляем данные о партии из redis.
class PlayerLoseAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        status = str(redis_conn.get(f'user_{user}_status').decode('utf-8').replace("'", '"'))
        if status == 'more':
            delete_session_data(user)
            return Response({"message": "Игра завершина. Пользователь перебрал карты и потерял ставку"})
        if status == 'double':
            delete_session_data(user)
            return Response({"message": "Игра завершина. Пользователь удвоил и перебрал карты"})


# Игрок может отказаться от карт, тогда для более читаемого кода лечке сразу обработать этот сценарий
class PlayerRefundAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        bet = int(redis_conn.get(f'user_{user}_bet'))
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance += int(bet * 0.5)
        balance_object.save()
        delete_session_data(user)
        return Response({"message": "Игра завершина. Пользователь вернул карты и потерял половину ставки"})


# Здесь происходит списание ставок с баланса
class ReduceBalance(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        bet = int(redis_conn.get(f'user_{user}_bet'))
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance -= int(bet)
        balance_object.save()
        return Response({"message": "Ставка принята"})


# Реализация ходов диллера
class DealerTurn(APIView):
    def get(self, request):
        # Берем информацию о игроке, колоде(преобразуем её, тк редис хранит в двоичном представлении) и руке диллера
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        cards = json.loads(redis_conn.get(f'user_{user}_cards_deck').decode('utf-8').replace("'", '"'))
        cards = Deck(cards)
        dealer_hand = json.loads(redis_conn.get(f'user_{user}_dealer_hand').decode('utf-8'))
        dealer_hand = Hand(dealer_hand['cards'], dealer_hand['value'])
        dealer_hand.hidden = False
        # Далее по правилам BlackJack диллер берет карты, пока не наберется 17 или более.
        while dealer_hand.value < 17:
            dealer_hand.add_card(cards.take_card())
        # Сериализуем данные для отправки
        dealer_hand_serializer = HandSerializer(dealer_hand)
        response_data = {
            "dealer_hand": dealer_hand_serializer.data,
        }
        # Храним в redis информацию о картах и состоянии колоды
        redis_conn.set(f'user_{user}_dealer_hand', json.dumps(dealer_hand_serializer.data))
        redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))
        return Response(response_data)


# Записываем в redis, что игрок больше не берет карты и отправляем это на клиент, чтобы начался ход диллера
class PlayerStop(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        redis_conn.set(f'user_{user}_status', 'stop')
        return Response({"message": "Игрок не добирает карты"})


# Определение результата игры
class ResultGameAPI(APIView):
    def get(self, request):
        # Берем пользователя, информацию о том, какие были ставки(status) и саму ставку
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        status = str(redis_conn.get(f'user_{user}_status').decode('utf-8').replace("'", '"'))
        bet = int(redis_conn.get(f'user_{user}_bet'))

        # Определяем, сколько очков у игрока и у диллера
        dealer_hand = json.loads(redis_conn.get(f'user_{user}_dealer_hand').decode('utf-8'))
        dealer_hand = Hand(dealer_hand['cards'], dealer_hand['value'])

        player_hand = json.loads(redis_conn.get(f'user_{user}_player_hand').decode('utf-8'))
        player_hand = Hand(player_hand['cards'], player_hand['value'])

        player_value = player_hand.value
        dealer_value = dealer_hand.value

        # Если игрок сразу поймал BJ, то он будет отправлен на этот апи и ему выплатится его ставка 3 : 2
        if status == 'blackjack':
            balance_object = UserBalance.objects.get(user=user)
            balance_object.balance += int(bet) * 3
            balance_object.save()
            delete_session_data(user)
            return Response({"game": "blackjack"})

        # Если дилер перебрал либо игрок набрал больше, в зависимости от того, какие были ставки(status), баланс
        # пополняется и отпровляется сообщение о победе, чтобы отоброзить соответствующую информацию у пользователя.
        if dealer_value > 21 or player_value > dealer_value:
            if status == 'double':
                balance_object = UserBalance.objects.get(user=user)
                balance_object.balance += int(bet) * 4
                balance_object.save()
            else:
                balance_object = UserBalance.objects.get(user=user)
                balance_object.balance += int(bet) * 2
                balance_object.save()
                delete_session_data(user)
            return Response({"game": "win"})

        # Если счет совпал, происходит возврат
        elif player_value == dealer_value:
            if status == 'double':
                balance_object = UserBalance.objects.get(user=user)
                balance_object.balance += int(bet) * 2
                balance_object.save()
            else:
                balance_object = UserBalance.objects.get(user=user)
                balance_object.balance += int(bet)
                balance_object.save()
                delete_session_data(user)
            return Response({"game": "draw"})

        # Если игрок проиграл, баланс его не меняется, так как он уже списался при начале игры
        elif dealer_value > player_value:
            delete_session_data(user)
            return Response({"game": "lose"})


# Возвращаем топ 10 рекордов
class RecordAPI(APIView):
    def get(self, request):
        records = UserBalance.objects.all()
        records = [[i.user.username, i.record] for i in records]
        records.sort(reverse=True, key=lambda x: x[1])
        records = records[:5]
        return Response({"top": records})
