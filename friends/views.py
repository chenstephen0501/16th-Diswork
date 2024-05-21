from django.views.generic import ListView, DeleteView
from .models import Friend
from members.models import Member
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class MemberListView(ListView):
    model = Member
    template_name = "search/search_list.html"
    context_object_name = "search_list"
    def get_queryset(self):
            query = super().get_queryset()
            keyword = self.request.GET.get("username", "").strip()
            if keyword:
                return query.filter(name__icontains=keyword)
            return query
    

@method_decorator(login_required, name="dispatch")
class FriendListView(ListView):
    model = Friend
    paginate_by = 5


@method_decorator(login_required, name="dispatch")
class FriendDeleteView(DeleteView):
    model = Friend
    template_name = "friends/confirm_delete.html"
    success_url = reverse_lazy("friends:friend_list")


@login_required
def send_friend_request(req, receiver_id):
    if req.method == "POST":
        sender_id = req.user.id
        receiver = get_object_or_404(Member, id=receiver_id)
        if sender_id == receiver_id:
            return HttpResponse("不能向自己發送好友邀請。")

        sender = get_object_or_404(Member, id=sender_id)

        friend_request, created = Friend.objects.get_or_create(
            sender=sender, receiver=receiver
        )
        if created:
            return HttpResponse("好友邀請已發送！")
        else:
            return HttpResponse("好友邀請已經發送過了！")
    return redirect("friends:friend_list")


@login_required
def accept_friend_request(req, friend_request_id):
    try:
        friend_request = Friend.objects.get(id=friend_request_id, status="等待確認")
    except Friend.DoesNotExist:
        return HttpResponse("好友邀請不存在或已處理。")

    if friend_request.receiver == req.user:
        sender = friend_request.sender
        receiver = friend_request.receiver

        receiver.friends.add(sender)
        sender.friends.add(receiver)

        friend_request.status = "確認"
        friend_request.save()

        return HttpResponse("好友邀請已接受！")
    else:
        return HttpResponse("好友邀請未被接受。")


@login_required
def reject_friend_request(req, friend_request_id):
    if req.method == "POST":
        friend_request = get_object_or_404(
            Friend, id=friend_request_id, status="等待確認"
        )
        if friend_request.receiver == req.user:
            friend_request.status = "已拒絕"
            friend_request.save()
            return HttpResponse("好友邀請已拒絕。")
        return HttpResponse("好友邀請未被拒絕。")
    return redirect("friend_requests")


@login_required
def friend_requests(req):
    received_requests = Friend.objects.filter(receiver=req.user, status="等待確認")
    return render(
        req, "friends/friend_requests.html", {"received_requests": received_requests}
    )
