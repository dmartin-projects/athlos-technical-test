from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.scrapper.scraper_engine import ScrapperEngine
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.scrapper.scraper_engine import ScrapperEngine
from django.shortcuts import get_object_or_404


import logging

from apps.scrapper.models import Hotel
from apps.scrapper.serializers import CreateHotelSerializer, HotelSerializer, ScrapedHotelDataSerializer

logger = logging.getLogger("django")

from rest_framework.views import APIView



@api_view(['GET','DELETE'])
def get_hotel_by_id(request, id:str):
    """Gets a specific hotel by ID"""
    try:
        if request.method == 'DELETE':
            hotel = get_object_or_404(Hotel, pk=id)
            hotel_name = hotel.name
            hotel.delete()
            logger.info(f"Hotel '{hotel_name}' (ID: {id}) deleted successfully")
            return Response({"ok": True, "data": None, "msg": f"Hotel '{hotel_name}' deleted successfully"}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            hotel = get_object_or_404(Hotel, pk=id)
            serializer = HotelSerializer(hotel)
            return Response({"ok": True,"data": serializer.data,"msg": "Hotel retrieved successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error getting hotel {id}: {str(e)}")
        return Response({"ok": False,"msg": f"An unexpected error occurred retrieving or deleting Hotel with ID {id}","error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_hotel_scrape_data(request):
    """Scrapes Booking.com to get hotel data without saving to database"""
    search_query = request.GET.get('name', '')
    try:

        if not search_query:
            return Response({"ok": False,"msg": "Hotel name parameter is required","error": "Missing required parameter 'name'"}, status=status.HTTP_400_BAD_REQUEST)
            
        search_query = '+'.join(search_query.strip().split())
        logger.info(f"Starting hotel scraping for: {search_query}")

        scrapper = ScrapperEngine()
        hotel_data = scrapper.scrape_url(f"https://www.booking.com/searchresults.es.html?ss={search_query}&checkin=2025-12-28&checkout=2025-12-29&group_adults=2&group_children=0&no_rooms=1&selected_currency=EUR")
       
        serializer = ScrapedHotelDataSerializer(data=hotel_data)
        if serializer.is_valid():
            logger.info(f"Hotel data scraped successfully for: {search_query}")
            return Response({"ok": True,"data": serializer.data,"msg": f"Hotel data scraped successfully for '{search_query}'"}, status=status.HTTP_200_OK)
        else:
            logger.error(f"Serializer validation failed for {search_query}: {serializer.errors}")
            return Response({"ok": False,"msg": "Invalid scraped data format","error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error scraping hotel data for '{search_query}': {str(e)}")
        return Response({"ok": False,"msg": f"Error scraping hotel data","error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
@extend_schema(
      summary="Create Hotel",
      description="Create new hotel from JSON",
      request={
          'application/json': {
              'type': 'object',
              'example': {
                  "name": "Hotel Barcelona Plaza",
                  "location": "Barcelona, España",
                  "description": "Una descripción...",
                  "review_mark": 4.5,
                  "comments": 120,
                  "photo_urls": ["https://cf.bstatic.com/xdata/images/hotel/max1024x768/718967467.jpg?k=cf903adb06ada89d296ab42792824822c4d5dc40863d0aaba35738530819006f&o="],
                  "amenities": ["Pool", "WiFi", "Gym"],
                  "average_price": 453.8
              }
          }
      },
      responses={201: "Hotel created successfully"}
  )
@api_view(['POST','GET'])
def hotels(request):
    try:
        if request.method == 'GET':
            hotels = Hotel.objects.all()
            serializer = HotelSerializer(hotels, many=True)
            logger.info(f"Retrieved {len(hotels)} hotels from database")
            return Response({"ok": True,"data": serializer.data,"msg": f"Successfully retrieved {len(hotels)} hotels"}, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            if not request.data:
                return Response({"ok": False,"msg": "Request body is required","error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)

            serializer_data = CreateHotelSerializer(data=request.data)
            if serializer_data.is_valid():
                hotel = serializer_data.save()
                logger.info(f"Hotel '{hotel.name}' created successfully with ID: {hotel.id}")
                return Response({"ok": True,"data": {"hotel_id": hotel.id},"msg": f"Hotel '{hotel.name}' created successfully"}, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Hotel creation failed: {serializer_data.errors}")
                return Response({"ok": False,"msg": "Invalid hotel data provided","error": serializer_data.errors}, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        logger.error(f"Unexpected error in hotels endpoint: {str(e)}")
        return Response({"ok": False,"msg": "An unexpected error occurred","error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

