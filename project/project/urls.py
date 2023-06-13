from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # url для стартовой страницы и чатов
    path('', include('chat.urls')),
    # url для страницы администратора
    path('admin/', admin.site.urls),
    # url для REST API Framework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url для регистрации, авторизации, просмотра профиля пользователей,
    # просмотра списка пользователей
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

# взаимодейсивие url с папками медиа-контента (аватарами) пользователей
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
