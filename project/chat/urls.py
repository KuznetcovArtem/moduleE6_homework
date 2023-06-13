from django.urls import path
from .views import index, room_create, room_update, RoomDelete, room

urlpatterns = [
    # url для входа на сайт
    path('', index, name='index'),
    # url для создания чата
    path('chat/create/', room_create, name='room_create'),
    # url для изменения созданного ранее чата
    path('chat/<int:pk>/update/', room_update, name='room_update'),
    # url для удаления созданного ранее чата
    path('chat/<int:pk>/delete/', RoomDelete.as_view(), name='room_delete'),
    # url для входа в чат
    path('chat/<str:room_name>/', room, name='room'),
]
