from django_redis import get_redis_connection


def delete_session_data(user):
    redis_conn = get_redis_connection("default")
    redis_conn.delete(f'user_{user}_status')
    redis_conn.delete(f'user_{user}_bet')
    redis_conn.delete(f'user_{user}_cards_deck')
    redis_conn.delete(f'user_{user}_player_hand')
    redis_conn.delete(f'user_{user}_dealer_hand')