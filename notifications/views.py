from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from boards.models import Category


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-date_sent"
    )
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    category_list = Category.objects.all()
    return render(
        request,
        "notifications/notification_list.html",
        {
            "notifications": notifications,
            "unread_count": unread_count,
            "category_list": category_list,
        },
    )


@login_required
def delete_notification(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    if notification.user == request.user:
        notification.delete()
    return redirect("notifications:list")


@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(
        Notification, id=notification_id, user=request.user
    )
    notification.is_read = True
    notification.save()
    return redirect("notifications:list")
