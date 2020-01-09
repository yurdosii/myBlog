from django.db import models


class Subscriber(models.Model):
    email               = models.EmailField()
    unsubscribe_code    = models.CharField(max_length=120, blank=True, null=True)
    is_active           = models.BooleanField(default=True) 

    def __str__(self):
        return f"User {self.id} - {self.email}"

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
