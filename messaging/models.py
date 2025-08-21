from django.db import models
from django.contrib.auth.models import User

def message_image_path(instance, filename):
    return f'message_images/{instance.sender_id}/{filename}'

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conv_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conv_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def participants(self):
        return {self.user1_id, self.user2_id}

    def other_of(self, user):
        return self.user2 if user == self.user1 else self.user1

    def __str__(self):
        return f'Conversation {self.user1.username} <-> {self.user2.username}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to=message_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Msg from {self.sender.username} at {self.created_at}'