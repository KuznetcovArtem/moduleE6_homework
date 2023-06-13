from django.urls import path
from .views import signup, profile, profile_edit, user_list

urlpatterns = [
    # url для регистрации нового пользователя
    path('signup/', signup, name='signup'),
    # url для просмотра профиля пользователя
    path('profile/', profile, name='profile'),
    # url для изменения профиля пользователя
    path('profile_edit/', profile_edit, name='profile_edit'),
    # url для просмотра списка пользователей и менеджмента чатов
    path('user_list/', user_list, name='user_list'),
]
