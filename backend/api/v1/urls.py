from django.urls import path, include

urlpatterns = [
    path('hotels/', include('api.v1.scrapper.urls')),
]