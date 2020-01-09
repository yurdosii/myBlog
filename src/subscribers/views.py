from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView

from .models import Subscriber
from .utils import code_generator


class SubscribeView(CreateView):
    # як я поняв оце модель і поля щоб можна було на темплейті зробити form.as_p
    # model = Subscriber  # ПОХОДУ ЩЕ дЛЯ ТОГО ЩОБ ТУ ВАЛІДАЦІЮ РІЗНУ РОБИТИ
    # fields = [field.name for field in Subscriber._meta.fields]

    def post(self, request):
        print(request.POST)
        unsubscribe_code = code_generator()
        subscriber, created = Subscriber.objects.get_or_create(email=request.POST["email"], defaults={"unsubscribe_code": unsubscribe_code})
        print(subscriber, created)

        if not created:
            unsubscribe_code = subscriber.unsubscribe_code
            subscriber.is_active=True
            subscriber.save()

        subject = "Welcome to YuraBlog"
        from_email = ''
        message = 'Thanks for subscribe. Welcome to YuraBlog family.'
        # відправляємо на ту пошту що прийшла, а коли пост то на всі активні
        # recipient_list = ['magame@simplemail.top']
        recipient_list = [request.POST["email"]]
        path_ = reverse('subscribers:unsubscribe', kwargs={"code": unsubscribe_code})
        html_message = f"""
                <p>Welcome to YuraBlog family.</p>
                <p>Thanks for subscribe. Now you will be notificated about all my new posts.</p> <br>
                <p>You can unsubscribe here - <a href="{path_}">Unsubscribe</a> </p>
            """

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=html_message
        )

        return redirect(reverse("blog:home", kwargs=[]))


def unsubscribe_view(request, code=None, *args, **kwargs):
    # print(code)
    if code is not None:
        qs = Subscriber.objects.all().filter(unsubscribe_code=code)
        if qs.exists():
            subscriber = qs.first()
            subscriber.is_active = False
            subscriber.save()

    return redirect(reverse("blog:home", kwargs=[]))
