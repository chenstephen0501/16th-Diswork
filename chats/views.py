from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup
from .forms import ChatmessageCreateForm

def chat_view_home(request):
    chat_groups = ChatGroup.objects.all()
    return render(request, "chats/chat_home.html", {"chat_groups": chat_groups})

def chat_view_new(request):
    return render(request, "chats/chat_create.html")


# @login_required
def chat_view_show(request, id):
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
            # return redirect('chats:home')
            return redirect('chats:show', id=chat_group.id)
    return render(request, "chats/chat_group.html", {'chat_messages': chat_messages, 'form': form})

def chat_view_create(request):
    # chat_group_name = ChatGroup.objects.all()
    if request.method == 'POST':
        chat_group = ChatGroup(
            group_name = request.POST['group_name']
        )
        chat_group.save()
    return redirect('chats:home')

