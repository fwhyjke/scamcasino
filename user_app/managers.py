from django.contrib.auth.base_user import BaseUserManager


# Самописный менеджер для работы с пользователями. Необходим для кастомной модели пользователя
class UserManager(BaseUserManager):
    use_in_migrations = True

    # Приватный метод, который используется только внутри методов класса для создания пользователей
    def _create_user(self, username, password, **extra_fields):
        # Если пользователь не ввел логин, выдать ошибку
        if not username:
            raise ValueError('Field "username" must be set')

        # Записываем пользователя в БД
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Пришлось прибегнуть к такому import во избежание каскодного взаимодействия.
        # Сразу при регистрации пользователь получает баланс, что отображется в другой таблице
        from game_logic_api.models import UserBalance
        UserBalance.objects.create(user=user)

        return user

    # Если создается обычный пользователь, то он не имеет право пользоваться админ-панелью
    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username=username, password=password, **extra_fields)

    # Создание суперпользователя
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(username=username, password=password, **extra_fields)
