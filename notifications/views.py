from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-date_sent"
    )
    return render(
        request,
        "notifications/notification_list.html",
        {"notifications": notifications},
    )


@login_required
def delete_notification(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    if notification.user == request.user:
        notification.delete()
    return redirect("notifications:list")


@login_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    if notification.user == request.user:
        notification.is_read = True
        notification.save()
    return redirect("notifications:list")
