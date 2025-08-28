from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.scrapper_test, name='scrape_test'),
]