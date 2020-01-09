from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse

from .models import ContactMessage

# def home_page(request):
#     template_name = 'landing/home.html'
#     context = {}
#     return render(request, template_name, context)

class ContactMessageCreateView(CreateView):
    model = ContactMessage
    template_name = 'landing/contact.html'
    fields = [field.name for field in ContactMessage._meta.fields]

    # def post(self, request):
    #     super().post(request)
    #     print(request.POST)

    #     return redirect(reverse("contact", kwargs=[]))
