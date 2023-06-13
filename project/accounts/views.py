from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserEditForm, ChatUserEditForm
from chat.models import ChatUser, Room


# Представление для регистрации нового пользователя
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save form in the memory (not in database)
            user = form.save(commit=False)
            user.save()
            # Создаём экземпляр пользователя чата, у которого поле user - вновь созданный пользователь
            ChatUser.objects.create(user=user)
            return redirect('login')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


# Представление для отображения профиля пользователя
@login_required
def profile(request):
    # проверка, если пользователь зарегистрирован не через сайт (а, например, через cretesuperuser)
    # в этом случае создаётся экземпляр класса ChatUser с request.user в поле user
    if not ChatUser.objects.filter(user=request.user).exists():
        ChatUser.objects.create(user=request.user)
    return render(request, 'profile.html', {'user': ChatUser.objects.get(user=request.user)})


# Представление для редактирования профиля пользователя
@login_required
def profile_edit(request):
    chat_user = ChatUser.objects.get(user=request.user)
    if request.method == 'POST':
        # Данные берутся из двух разных форм
        user_form = UserEditForm(instance=request.user, data=request.POST)
        chat_user_form = ChatUserEditForm(instance=chat_user, data=request.POST, files=request.FILES)
        if user_form.is_valid() and chat_user_form.is_valid():
            user_form.save()
            chat_user_form.save()
            return redirect('profile')
        else:
            return render(request, 'profile_edit.html',
                          {'user_form': user_form,
                           'chat_user_form': chat_user_form})
    else:
        user_form = UserEditForm(instance=request.user)
        chat_user_form = ChatUserEditForm(instance=chat_user)
        return render(request, 'profile_edit.html',
                      {'user_form': user_form,
                       'chat_user_form': chat_user_form})


# Представление для отображения списка пользователей и менеджмента чатов
@login_required
def user_list(request):
    current_user = ChatUser.objects.get(user=request.user)
    users = ChatUser.objects.exclude(user=request.user)
    rooms = [room for room in Room.objects.all() if current_user in room.users.all() or current_user.user.is_staff]
    return render(request, 'user_list.html',
                  {'current_user': current_user,
                   'users': users,
                   'rooms': rooms})
