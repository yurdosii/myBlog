from django.contrib import admin

from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContactMessage._meta.fields]

    class Meta:
        model = ContactMessage

admin.site.register(ContactMessage, ContactMessageAdmin)