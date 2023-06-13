from django import forms
from .models import Room


# Форма создания и редактирования чата
class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'users']
