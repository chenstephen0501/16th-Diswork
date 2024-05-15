from django.db import models
from django.conf import settings

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique = True)

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name = 'chat_messages', on_delete = models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length = 300)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['-created_at']

class PrivateMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete = models.CASCADE, related_name = 'private_messages',
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"     

    class Meta:
        ordering= ['-created_at']  