from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.scrapper.scraper_engine import ScrapperEngine
from drf_spectacular.utils import extend_schema

import logging

logger = logging.getLogger("django")

from rest_framework.views import APIView


'''
como son endpoint simples usaré FBV en lugar de class-based-views
'''

@extend_schema(
      summary="Scrape URL",
      description="Realiza scrapping de una URL específica",
      responses={200: "Scrapping exitoso"}
  )
@api_view(['GET'])
def scrapper_test(request):

    logger.error("entra en la funcion ")
    
    return Response({
        'message': 'Scrapping initiated',
        'data': "hello world"
    }, status=status.HTTP_200_OK)

