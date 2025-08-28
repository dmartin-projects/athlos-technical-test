from django.urls import path, include

urlpatterns = [
    path('scrapper/', include('api.v1.scrapper.urls')),
]