from django_redis import get_redis_connection


# Вспомогательная функция, которая одним вызовом отчищает все данные о прошедшей игровой сессии в redis.
# Необходимо для того, чтобы при обновлении страници пользователь не мог манипулировать балансом.
def delete_session_data(user):
    redis_conn = get_redis_connection("default")
    redis_conn.delete(f'user_{user}_status')
    redis_conn.delete(f'user_{user}_bet')
    redis_conn.delete(f'user_{user}_cards_deck')
    redis_conn.delete(f'user_{user}_player_hand')
    redis_conn.delete(f'user_{user}_dealer_hand')