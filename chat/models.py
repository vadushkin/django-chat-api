from django.db import models
from users.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(
        to=CustomUser,
        related_name="message_sender",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        to=CustomUser,
        related_name="message_receiver",
        on_delete=models.CASCADE
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The message between {self.sender.username} & {self.receiver.username}"

    class Meta:
        ordering = ("-created_at",)


class MessageAttachment(models.Model):
    message = models.ForeignKey(
        to=Message,
        related_name="message_attachments",
        on_delete=models.CASCADE
    )
    attachment = models.ImageField(null=True, blank=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
