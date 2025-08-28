import pytest
from django.test import Client
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """
    Fixture para cliente de API de DRF
    """
    return APIClient()


@pytest.fixture
def django_client():
    """
    Fixture para cliente de Django
    """
    return Client()