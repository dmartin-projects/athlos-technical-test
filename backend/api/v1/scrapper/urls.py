from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotels, name='hotels'),
    path('<int:id>/', views.get_hotel_by_id, name='get_hotel_by_id'),
    path('scrape/', views.get_hotel_scrape_data, name='get_hotel_scrape_data'),
]