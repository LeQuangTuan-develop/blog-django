from django.urls import path

from module.ApiQuote.view import get_quote

urlpatterns = [
    path('random-quote/', get_quote),
]
