from django.views.generic import ListView, DeleteView
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Friend, Card
from members.models import Member
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from lib.paginate_que import paginate_queryset
import random
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.template.loader import render_to_string
from django.views import View


@method_decorator(login_required, name="dispatch")
class MemberListView(ListView):
    model = Member
    template_name = "friends/search_list.html"
    context_object_name = "search_list"
    paginate_by = 5

    def get_queryset(self):
        query = super().get_queryset().exclude(username=self.request.user)
        keyword = self.request.GET.get("username", "").strip()
        if keyword:
            return query.filter(username__icontains=keyword)
        return query


@method_decorator(login_required, name="dispatch")
class FriendListView(ListView):
    model = Friend
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Friend.objects.filter(sender=user, status="2") | Friend.objects.filter(
            receiver=user, status="2"
        )


@method_decorator(login_required, name="dispatch")
class FriendDeleteView(DeleteView):
    model = Friend
    template_name = "friends/confirm_delete.html"
    success_url = reverse_lazy("friends:friend_list")


@login_required
def send_friend_request(req, receiver_id):
    try:
        receiver_id = int(receiver_id)
    except ValueError:
        messages.error(req, "無效的接收者ID")
        return redirect("friends:member_list")

    sender_id = req.user.id
    receiver_exists = Member.objects.filter(id=receiver_id).exists()
    if not receiver_exists:
        messages.error(req, "沒有這個使用者!")
        return redirect("friends:member_list")
    elif sender_id == receiver_id:
        messages.error(req, "操作錯誤!")
        return redirect("friends:member_list")

    if req.method == "POST":
        is_friend = Friend.objects.filter(Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id)).exists()
        friend = Friend.objects.filter(Q(sender_id=sender_id, receiver_id=receiver_id) | Q(sender_id=receiver_id, receiver_id=sender_id)).first()
        if is_friend:
            if friend.status == "2":
                messages.error(req, "己經是好友了。")
            elif friend.receiver_id == req.user.id:
                messages.error(req, "對方己發送好友通知，請到等待中加好友!")        
            else:    
                messages.error(req, "好友邀請已經發送過了！")
        else:
            Friend.objects.create(sender_id=sender_id, receiver_id=receiver_id)
            messages.success(req, "好友邀請已發送！")
    
    return redirect("friends:member_list")


@login_required
def accept_friend_request(req, friend_request_id):
    try:
        friend_request = Friend.objects.get(id=friend_request_id, status="1")
    except Friend.DoesNotExist:
        messages.error(req, "好友邀請已經發送過了！")
        return render(req, "friends/search_list.html")

    if friend_request.receiver == req.user:
        sender = friend_request.sender
        receiver = friend_request.receiver

        if not Friend.objects.filter(sender=receiver, receiver=sender).exists():
            receiver.friends.add(sender)
            sender.friends.add(receiver)

        friend_request.status = "2"
        friend_request.save()

        messages.success(req, "好友邀請已接受")
        return render(req, "friends/friend_list.html")
    else:
        messages.error(req, "好友邀請已接受")
        return render(req, "friends/friend_list.html")


@login_required
def reject_friend_request(req, friend_request_id):
    if req.method == "POST":
        friend_request = get_object_or_404(Friend, id=friend_request_id, status="1")
        if friend_request.receiver == req.user:
            friend_request.status = "3"
            friend_request.save()
    return redirect("friend_requests")


@login_required
def friend_requests(req):
    received_requests = Friend.objects.filter(receiver=req.user, status="1")
    return render(
        req, "friends/friend_requests.html", {"received_requests": received_requests}
    )


class DrawCardView(View):
    def get_queryset(self, user):
        friends = Friend.objects.filter(
            Q(sender=user, status="2") | Q(receiver=user, status="2")
        )

        friend_ids = set()
        for friend in friends:
            if friend.sender == user:
                friend_ids.add(friend.receiver.id)
            elif friend.receiver == user:
                friend_ids.add(friend.sender.id)

        return Member.objects.exclude(id__in=friend_ids).exclude(id=user.id)

    def get(self, request):
        user = request.user
        members = list(self.get_queryset(user))
        today = timezone.now().date()

        already_drew_today = (
            Card.objects.annotate(date=TruncDate("created_at"))
            .filter(drawer=user)
            .first()
        )

        if already_drew_today:
            random_member = already_drew_today.drawn
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                member_data = {
                    "id": random_member.id,
                    "username": random_member.username,
                    "name": random_member.name or "未填寫",
                    "user_img": (
                        random_member.user_img.url
                        if random_member.user_img
                        else "/static/image/cathead.png"
                    ),
                    "birthday": (
                        random_member.birthday.strftime("%Y-%m-%d")
                        if random_member.birthday
                        else "未知"
                    ),
                    "interest": random_member.interest or "未填寫",
                    "constellation": random_member.constellation or "未填寫",
                }
                return JsonResponse(member_data)
            else:
                return render(
                    request,
                    "friends/card.html",
                    {"drawn_member": random_member, "draw_limit_reached": True},
                )

        random_member = None

        random_member = random.choice(members)
        existing_card = Card.objects.filter(drawer=user, drawn=random_member).exists()

        card = Card.objects.create(drawer=user, drawn=random_member)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            member_data = {
                "id": random_member.id,
                "username": random_member.username,
                "name": random_member.name or "未填寫",
                "user_img": (
                    random_member.user_img.url
                    if random_member.user_img
                    else "/static/image/cathead.png"
                ),
                "birthday": (
                    random_member.birthday.strftime("%Y-%m-%d")
                    if random_member.birthday
                    else "未填寫"
                ),
                "interest": random_member.interest or "未填寫",
                "constellation": random_member.constellation or "未填寫",
            }
            return JsonResponse(member_data)
        else:
            return render(request, "friends/card.html", {"drawn_member": random_member})
