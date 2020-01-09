from django.db import models
from django.urls import reverse


class ContactMessage(models.Model):
    name    = models.CharField(max_length=128)
    email   = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Msg {self.id} - {self.name}, {self.email}, {self.message}"

    class Meta:
        verbose_name = 'Contact message'
        verbose_name_plural = 'Contact messages'

    def get_absolute_url(self):
        return reverse("contact")
