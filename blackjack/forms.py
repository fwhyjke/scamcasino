from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from user_app.models import User


# Форма регистрации пользователей
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        data = self.cleaned_data
        data['password'] = data.pop('password1')
        del data['password2']
        user = User.objects.create_user(**data)
        return user


# Форма для входа пользователей
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Введите ваш логин'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Введите ваш пароль'}))

    class Meta:
        fields = ['email', 'password']
