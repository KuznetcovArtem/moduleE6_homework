from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .forms import RoomCreateForm
from .models import Room, ChatUser, Message


# Представление для входа на сайт
def index(request):
    return render(request, "chat/index.html")


# Представление для входа в чат, доступно только авторизованному пользователю
@login_required
def room(request, room_name):
    current_room = Room.objects.get(name=room_name)
    # проверка уровня доступа текущего пользователя
    if request.user not in current_room.get_user_list() and not request.user.is_staff:
        raise PermissionDenied
    # адаптация названия чата для предотвращения ошибок,
    # возникающих при использовании спецсимволов в url
    room_name = room_name.replace(' ', '_').replace('/', '_').replace('!', '_').replace('=', '_')
    # return render(request, "chat/room.html", {"room_name": room_name})
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "username": request.user.username,
    })


# Представление для создания нового чата
@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            return render(request, 'room_create.html', {'form': form})
    else:
        form = RoomCreateForm()
        return render(request, 'room_create.html', {'form': form})


# Представление для обновления параметров (названия и списка пользователей) чата
# Выполняется только для авторизованного пользователя, имеющего доступ к чату
@login_required
def room_update(request, pk):
    current_room = Room.objects.get(pk=pk)
    # Проверка наличия доступа к выполнению функции у авторизованного пользователя
    if request.user not in current_room.get_user_list() and not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = RoomCreateForm(instance=current_room, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            return render(request, 'room_create.html', {'form': form})
    else:
        form = RoomCreateForm(instance=current_room)
        return render(request, 'room_create.html', {'form': form})


# Представление для удаления чата
# Выполняется только для авторизованного пользователя, имеющего доступ к чату
class RoomDelete(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'room_delete.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        obj = DeleteView.get_object(self, queryset=None)
        if self.request.user not in obj.get_user_list() and not self.request.user.is_staff:
            raise PermissionDenied
        return obj
