import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestScrapperEndpoints:
    
    def test_scrape_url_valid_request(self, api_client):

        url = reverse('scrape_url')
        data = {
            'url': 'https://example.com',
            'depth': 1
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 200
        assert 'message' in response.data
        assert 'data' in response.data
    
    def test_scrape_url_invalid_url(self, api_client):

        url = reverse('scrape_url')
        data = {
            'url': 'not-a-url',
            'depth': 1
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == 400
        assert 'url' in response.data