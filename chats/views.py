from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatGroup, PrivateChatRoom, PrivateMessage
from .forms import ChatmessageCreateForm
from members.models import Member
from friends.models import Friend
from boards.models import Category
from django.db.models import Q, Prefetch, OuterRef, Subquery
from django.core.paginator import Paginator
from django.db.models import Max, F

@login_required
def chat_home(request):
    chat_groups = ChatGroup.objects.all()
    return render(request, "chats/chat_home.html", {"chat_groups": chat_groups})


@login_required
def chat_new(request):
    return render(request, "chats/chat_create.html")


@login_required
def chat_show(request, id):
    chat_group = get_object_or_404(ChatGroup, pk=id)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return redirect("chats:show", id=chat_group.id)
    return render(
        request, "chats/chat_group.html", {"chat_messages": chat_messages, "form": form}
    )


@login_required
def chat_create(request):
    if request.method == "POST":
        group_name = request.POST["group_name"]
        if not ChatGroup.objects.filter(group_name=group_name).exists():
            chat_group = ChatGroup(group_name=group_name)
            messages.success(request, "新增成功")
            chat_group.save()
        else:
            messages.error(request, "群組名稱重複請更換名稱")
    return redirect("chats:home")


@login_required
def private_message_home(request):
    latest_messages_subquery = PrivateMessage.objects.filter(
        receiver_id=OuterRef('receiver_id'),
        sender_id=OuterRef('sender_id')
    ).order_by('-created_at').values('created_at')[:1]

    latest_messages = PrivateMessage.objects.filter(
        receiver_id=request.user.id,
        created_at=Subquery(latest_messages_subquery)
    ).select_related("sender", "private_room").order_by("-created_at")
    
    return render(request, "chats/private_message_home.html", {"private_messages": latest_messages})




@login_required
def private_message_room(request, room_name):
    privates_users = room_name.split("_")
    category_list = Category.objects.all()

    if (
        int(privates_users[0]) == request.user.id
        or int(privates_users[1]) == request.user.id
    ):
        check_private_room = PrivateChatRoom.objects.filter(
            room_name=room_name
        ).exists()
        if check_private_room:
            private_room = PrivateChatRoom.objects.prefetch_related(
                Prefetch(
                    "private_messages",
                    queryset=PrivateMessage.objects.select_related(
                        "sender", "receiver"
                    ),
                )
            ).get(room_name=room_name)
            receiver_id = next(
                user_id for user_id in privates_users if request.user.id != int(user_id)
            )
            receiver = Member.objects.get(id=receiver_id)
            private_messages = private_room.private_messages.all()

            return render(
                request,
                "chats/private_message_room.html",
                {
                    "room_name": room_name,
                    "private_messages": private_messages,
                    "receiver": receiver,
                    "category_list": category_list,
                },
            )

        else:
            receiver_id = next(
                user_id for user_id in privates_users if request.user.id != int(user_id)
            )
            receiver = Member.objects.get(id=receiver_id)
            return render(
                request,
                "chats/private_message_room.html",
                {"room_name": room_name, "receiver": receiver},
            )
    else:
        friend_list = Friend.objects.filter(
            Q(receiver_id=request.user.id)
            | Q(sender_id=request.user.id)
            & ~Q(receiver_id=request.user.id)
            & ~Q(sender_id=request.user.id)
            & Q(status=2)
        )
        messages.error(request, "操作錯誤")
        return render(request, "friends/friend_list.html", {"friend_list": friend_list})
