from django.urls import path

from .views import SubscribeView, unsubscribe_view


app_name = 'subscribers'

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:code>', unsubscribe_view, name='unsubscribe'),
]
