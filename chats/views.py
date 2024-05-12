from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatGroup
from .forms import ChatmessageCreateForm

def chat_home(request):
    chat_groups = ChatGroup.objects.all()
    return render(request, "chats/chat_home.html", {"chat_groups": chat_groups})

def chat_new(request):
    return render(request, "chats/chat_create.html")

def chat_show(request, id):
    chat_group = get_object_or_404(ChatGroup, pk = id)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return redirect('chats:show', id=chat_group.id)
    return render(request, "chats/chat_group.html", {'chat_messages': chat_messages, 'form': form})

def chat_create(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        if not ChatGroup.objects.filter(group_name = group_name).exists():
            chat_group = ChatGroup(group_name = group_name)
            messages.success(request, '新增成功')
            chat_group.save()
        else:
            messages.error(request, '群組名稱重複請更換名稱')

    return redirect('chats:home')

