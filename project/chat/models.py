from django.contrib.auth.models import User
from django.db import models
from PIL import Image


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/users/<username>/<filename>
    return f'users/{instance.user.username}/{filename}'


# Модель ChatUser
# Представляет собой встроенную модель User, но с картинкой-аватаром
class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='users/default.jpg')

    # метод отображения имени пользователя при обращении к экземпляру класса модели
    def __str__(self):
        return self.user.username

    # метод приведения аватара к стандартному размеру, вызывается при сохранении экземпляра модели
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.avatar.path)


# Модель Room
# Представляет собой модель чат-комнат
# name - уникальное название чата, строка диной 255 символов
# add_date - дата создания чата, заполняется автоматически
# users - список пользователей, которым разрешен доступ к чату,
# реляция многие ко многим с моделью ChatUser
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    add_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(ChatUser, related_name='users')

    # метод отображения названия чата при обращении к экземпляру класса модели
    def __str__(self):
        return self.name

    # метод возвращает список пользователей, которым разрешен доступ к чату
    def get_user_list(self):
        user_list = []
        for user in self.users.all():
            user_list.append(user.user)
        return user_list


# Модель Message
# Представляет собой модель сообщений, оставляемых собеседниками в чатах
# author - автор сообщения, реляция один ко многим с моделью ChatUser
# add_date - дата создания сообщения, заполняется автоматически
# text - текст сообщения
# room - комната, в которой сообщение было написано, реляция один ко многим с моделью Room
class Message(models.Model):
    author = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    add_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    # метод отображения текста сообщения при обращении к экземпляру класса модели
    def __str__(self):
        return self.text

    # метод возвращает при открытии чата последние 30 сообщений, написанных пользователями чата
    def last_30_messages(room_name):
        return Message.objects.filter(room__name=room_name).order_by('add_date')[:30]
