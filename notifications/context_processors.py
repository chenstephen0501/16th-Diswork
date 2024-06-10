from .models import Notification


def unread_notifications_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
    else:
        unread_count = 0
    return {"unread_count": unread_count}
