from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
import json

from apps.scrapper.models import Hotel, HotelPhoto, Amenity
from apps.scrapper.serializers import HotelSerializer, CreateHotelSerializer


class HotelEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.amenity1 = Amenity.objects.create(name="WiFi")
        self.amenity2 = Amenity.objects.create(name="Pool")
        
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            location="Test City",
            average_price=100.50,
            description="Test description",
            review_mark=8.5,
            comments=150
        )
        self.hotel.amenities.add(self.amenity1, self.amenity2)
        
        HotelPhoto.objects.create(
            hotel=self.hotel, 
            url="https://example.com/image1.jpg"
        )

    def test_get_hotels_success(self):
        response = self.client.get('/api/v1/hotels/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertTrue(data['ok'])
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], 'Test Hotel')

    def test_get_hotel_by_id_success(self):
        response = self.client.get(f'/api/v1/hotels/{self.hotel.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertTrue(data['ok'])
        self.assertEqual(data['data']['name'], 'Test Hotel')
        self.assertEqual(data['data']['location'], 'Test City')

    def test_get_hotel_by_id_not_found(self):
        response = self.client.get('/api/v1/hotels/999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.json()
        
        self.assertFalse(data['ok'])
        self.assertIn('not found', data['msg'])

    def test_create_hotel_success(self):
        hotel_data = {
            "name": "New Hotel",
            "location": "New City",
            "average_price": 200.00,
            "description": "New hotel description",
            "review_mark": 9.0,
            "comments": 200,
            "photo_urls": ["https://example.com/new1.jpg"],
            "amenities": ["Gym", "Spa"]
        }
        
        response = self.client.post(
            '/api/v1/hotels/', 
            data=json.dumps(hotel_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        
        self.assertTrue(data['ok'])
        self.assertIn('hotel_id', data['data'])
        
        new_hotel = Hotel.objects.get(id=data['data']['hotel_id'])
        self.assertEqual(new_hotel.name, 'New Hotel')

    def test_create_hotel_invalid_data(self):
        invalid_data = {
            "name": "",
            "location": "City",
            "review_mark": "invalid"
        }
        
        response = self.client.post(
            '/api/v1/hotels/', 
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        
        self.assertFalse(data['ok'])
        self.assertIn('error', data)

    def test_create_hotel_empty_body(self):
        response = self.client.post(
            '/api/v1/hotels/', 
            data='',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        
        self.assertFalse(data['ok'])
        self.assertEqual(data['msg'], 'Request body is required')

    def test_delete_hotel_success(self):
        hotel_id = self.hotel.id
        
        response = self.client.delete(f'/api/v1/hotels/{hotel_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertTrue(data['ok'])
        self.assertIn('deleted successfully', data['msg'])
        
        self.assertFalse(Hotel.objects.filter(id=hotel_id).exists())

    def test_delete_hotel_not_found(self):
        response = self.client.delete('/api/v1/hotels/999/')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        
        self.assertFalse(data['ok'])


class HotelScrapingEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('apps.scrapper.views.ScrapperEngine')
    def test_scrape_hotel_success(self, mock_scraper_class):
        mock_scraper = MagicMock()
        mock_scraper_class.return_value = mock_scraper
        
        mock_hotel_data = {
            'name': 'Scraped Hotel',
            'location': 'Barcelona, Spain',
            'average_price': 150.0,
            'description': 'Beautiful hotel',
            'review_mark': 8.0,
            'comments': 100,
            'photo_urls': ['https://example.com/img1.jpg'],
            'amenities': ['WiFi', 'Pool']
        }
        mock_scraper.scrape_url.return_value = mock_hotel_data
        
        response = self.client.get('/api/v1/hotels/scrape/?name=test+hotel')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        
        self.assertTrue(data['ok'])
        self.assertEqual(data['data']['name'], 'Scraped Hotel')
        mock_scraper.scrape_url.assert_called_once()

    def test_scrape_hotel_missing_name(self):
        response = self.client.get('/api/v1/hotels/scrape/')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        
        self.assertFalse(data['ok'])
        self.assertEqual(data['msg'], 'Hotel name parameter is required')

    @patch('apps.scrapper.views.ScrapperEngine')
    def test_scrape_hotel_scraper_error(self, mock_scraper_class):
        mock_scraper = MagicMock()
        mock_scraper_class.return_value = mock_scraper
        mock_scraper.scrape_url.side_effect = Exception("Scraping failed")
        
        response = self.client.get('/api/v1/hotels/scrape/?name=test+hotel')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        data = response.json()
        
        self.assertFalse(data['ok'])
        self.assertEqual(data['msg'], 'Error scraping hotel data')


class HotelModelsTestCase(TestCase):
    def test_hotel_creation(self):
        hotel = Hotel.objects.create(
            name="Model Test Hotel",
            location="Test Location",
            average_price=99.99,
            description="Test description",
            review_mark=7.5,
            comments=50
        )
        
        self.assertEqual(hotel.name, "Model Test Hotel")
        self.assertEqual(hotel.average_price, 99.99)
        self.assertTrue(isinstance(hotel.id, int))

    def test_hotel_photo_relationship(self):
        hotel = Hotel.objects.create(
            name="Photo Test Hotel",
            location="Test Location",
            average_price=100.0,
            review_mark=8.0,
            comments=100
        )
        
        photo1 = HotelPhoto.objects.create(
            hotel=hotel, 
            url="https://example.com/photo1.jpg"
        )
        photo2 = HotelPhoto.objects.create(
            hotel=hotel, 
            url="https://example.com/photo2.jpg"
        )
        
        self.assertEqual(hotel.photo_urls.count(), 2)
        self.assertIn(photo1, hotel.photo_urls.all())
        self.assertIn(photo2, hotel.photo_urls.all())

    def test_hotel_amenity_relationship(self):
        hotel = Hotel.objects.create(
            name="Amenity Test Hotel",
            location="Test Location",
            average_price=100.0,
            review_mark=8.0,
            comments=100
        )
        
        amenity1 = Amenity.objects.create(name="Free WiFi")
        amenity2 = Amenity.objects.create(name="Swimming Pool")
        
        hotel.amenities.add(amenity1, amenity2)
        
        self.assertEqual(hotel.amenities.count(), 2)
        self.assertIn(amenity1, hotel.amenities.all())
        self.assertIn(amenity2, hotel.amenities.all())


class HotelSerializersTestCase(TestCase):
    def test_hotel_serializer(self):
        amenity = Amenity.objects.create(name="Test Amenity")
        hotel = Hotel.objects.create(
            name="Serializer Test Hotel",
            location="Test Location",
            average_price=100.0,
            description="Test description",
            review_mark=8.0,
            comments=100
        )
        hotel.amenities.add(amenity)
        
        HotelPhoto.objects.create(
            hotel=hotel, 
            url="https://example.com/test.jpg"
        )
        
        serializer = HotelSerializer(hotel)
        data = serializer.data
        
        self.assertEqual(data['name'], 'Serializer Test Hotel')
        self.assertEqual(len(data['amenities']), 1)
        self.assertEqual(len(data['photo_urls']), 1)

    def test_create_hotel_serializer(self):
        data = {
            'name': 'Create Test Hotel',
            'location': 'Create Test Location',
            'average_price': 150.0,
            'description': 'Create test description',
            'review_mark': 9.0,
            'comments': 200,
            'photo_urls': ['https://example.com/create1.jpg', 'https://example.com/create2.jpg'],
            'amenities': ['Create WiFi', 'Create Pool']
        }
        
        serializer = CreateHotelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        hotel = serializer.save()
        
        self.assertEqual(hotel.name, 'Create Test Hotel')
        self.assertEqual(hotel.photo_urls.count(), 2)
        self.assertEqual(hotel.amenities.count(), 2)
        self.assertTrue(Amenity.objects.filter(name='Create WiFi').exists())
        self.assertTrue(Amenity.objects.filter(name='Create Pool').exists())