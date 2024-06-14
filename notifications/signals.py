from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notification
from friends.models import Friend
from chats.models import PrivateMessage
from comments.models import Comment, LikeComment
from articles.models import LikeArticle
from django.utils.html import format_html
from django.urls import reverse


@receiver(post_save, sender=Friend)
def handle_friend(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            title="好友邀請",
            message=f"{instance.sender.username} 要求加你好友。",
        )


@receiver(post_save, sender=PrivateMessage)
def handle_message(sender, instance, created, **kwargs):
    if created:

        if instance.sender.id < instance.receiver.id:
            room_name = f"{instance.sender.id}_{instance.receiver.id}"
        else:
            room_name = f"{instance.receiver.id}_{instance.sender.id}"
        chat_url = reverse("chats:private_message_room", args=[room_name])
        notification_message = format_html(
            '{} 傳了一則私訊。<a href="{}">點擊這裡查看</a>',
            instance.sender.username,
            chat_url,
        )

        Notification.objects.create(
            user=instance.receiver,
            title="新訊息",
            message=notification_message,
        )


@receiver(post_save, sender=Comment)
def handle_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.article.author,
            title="新留言",
            message=f"{instance.member.username} 在你的文章底下留言。",
        )


@receiver(post_save, sender=LikeArticle)
def handle_like_article(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.like_article.author,
            title="新的文章按讚",
            message=f"{instance.like_by_article.username} 說你的文章讚。",
        )


@receiver(post_save, sender=LikeComment)
def handle_like_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.like_comment.member,
            title="新的留言按讚",
            message=f"{instance.like_by.username} 說你的留言讚。",
        )
