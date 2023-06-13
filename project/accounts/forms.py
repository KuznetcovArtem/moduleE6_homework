from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chat.models import ChatUser


# Форма для регистрации нового пользователя
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )


# Форма для изменения имени пользователя
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


# Форма для изменения аватара пользователя
class ChatUserEditForm(forms.ModelForm):
    class Meta:
        model = ChatUser
        fields = ['avatar']
