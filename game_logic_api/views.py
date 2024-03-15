import json
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView
from game_logic_api.models import UserBalance
from game_logic_api.serializers import BalanceSerializer, HandSerializer
from game_logic_api.logic import Deck, Hand
from game_logic_api.utils import delete_session_data


class GetUserBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance = dict(BalanceSerializer(balance_object).data)
        if balance['balance'] > balance['record']:
            balance_object.record = balance['balance']
            balance_object.save()
        return Response({'bal': balance['balance'], 'rec': balance['record']})


class ResetBalanceAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance = 5000
        balance_object.save()
        return Response({"message": "Баланс успешно сброшен"})


class StartGameAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        bet = request.query_params.get('bet')
        cards = Deck([])
        # перемешанная колода
        cards.shuffle_deck()
        player_hand = Hand(-1, -1)
        dealer_hand = Hand(-1, -1, hidden=True)
        for _ in range(2):
            player_hand.add_card(cards.take_card())
            dealer_hand.add_card(cards.take_card())

        player_hand_serializer = HandSerializer(player_hand)
        dealer_hand_serializer = HandSerializer(dealer_hand)

        if player_hand.value == 21:
            response_data = {
                "player_hand": player_hand_serializer.data,
                "dealer_hand": dealer_hand_serializer.data,
                "blackjack": 1
            }
            redis_conn = get_redis_connection("default")
            redis_conn.set(f'user_{user}_status', 'blackjack')
        else:
            response_data = {
                "player_hand": player_hand_serializer.data,
                "dealer_hand": dealer_hand_serializer.data,
                "blackjack": 0
            }

        redis_conn = get_redis_connection("default")
        redis_conn.set(f'user_{user}_bet', bet)
        redis_conn.set(f'user_{user}_player_hand', json.dumps(player_hand_serializer.data))
        redis_conn.set(f'user_{user}_dealer_hand', json.dumps(dealer_hand_serializer.data))
        redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))

        return Response(response_data)


class PlayerTurnAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        turn = request.query_params.get('turn')
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


class ReduceBalance(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        bet = int(redis_conn.get(f'user_{user}_bet'))
        balance_object = UserBalance.objects.get(user=user)
        balance_object.balance -= int(bet)
        balance_object.save()
        return Response({"message": "Ставка принята"})


class DealerTurn(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        cards = json.loads(redis_conn.get(f'user_{user}_cards_deck').decode('utf-8').replace("'", '"'))
        cards = Deck(cards)
        dealer_hand = json.loads(redis_conn.get(f'user_{user}_dealer_hand').decode('utf-8'))
        dealer_hand = Hand(dealer_hand['cards'], dealer_hand['value'])
        dealer_hand.hidden = False
        while dealer_hand.value < 17:
            dealer_hand.add_card(cards.take_card())
        dealer_hand_serializer = HandSerializer(dealer_hand)
        response_data = {
            "dealer_hand": dealer_hand_serializer.data,
        }
        redis_conn.set(f'user_{user}_dealer_hand', json.dumps(dealer_hand_serializer.data))
        redis_conn.set(f'user_{user}_cards_deck', json.dumps(cards.deck))
        return Response(response_data)


class PlayerStop(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        redis_conn.set(f'user_{user}_status', 'stop')
        return Response({"message": "Игрок не добирает карты"})


class ResultGameAPI(APIView):
    def get(self, request):
        user = request.query_params.get('id')
        redis_conn = get_redis_connection("default")
        status = str(redis_conn.get(f'user_{user}_status').decode('utf-8').replace("'", '"'))
        bet = int(redis_conn.get(f'user_{user}_bet'))
        
        dealer_hand = json.loads(redis_conn.get(f'user_{user}_dealer_hand').decode('utf-8'))
        dealer_hand = Hand(dealer_hand['cards'], dealer_hand['value'])

        player_hand = json.loads(redis_conn.get(f'user_{user}_player_hand').decode('utf-8'))
        player_hand = Hand(player_hand['cards'], player_hand['value'])

        player_value = player_hand.value
        dealer_value = dealer_hand.value

        if status == 'blackjack':
            balance_object = UserBalance.objects.get(user=user)
            balance_object.balance += int(bet) * 3
            balance_object.save()
            delete_session_data(user)
            return Response({"game": "blackjack"})

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

        elif dealer_value > player_value:
            delete_session_data(user)
            return Response({"game": "lose"})
