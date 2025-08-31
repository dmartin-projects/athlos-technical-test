from rest_framework import serializers
from .models import Hotel, HotelPhoto, Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['id', 'url']


class HotelSerializer(serializers.ModelSerializer):
    photo_urls = HotelPhotoSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Hotel
        fields = [
            'id',
            'name', 
            'location',
            'average_price',
            'description',
            'review_mark',
            'comments',  
            'amenities',
            'photo_urls'
        ]

class ScrapedHotelDataSerializer(serializers.Serializer):
   
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    average_price = serializers.FloatField()
    description = serializers.CharField(allow_blank=True, allow_null=True)
    review_mark = serializers.FloatField()
    comments = serializers.IntegerField()
    photo_urls = serializers.ListField(
        child=serializers.CharField(), 
        allow_empty=True
    )
    amenities = serializers.ListField(
        child=serializers.CharField(), 
        allow_empty=True
    )


class CreateHotelSerializer(serializers.ModelSerializer):

    photo_urls = serializers.ListField(
        child=serializers.URLField(),
        allow_empty=True,
        write_only=True
    )
    amenities = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        write_only=True
    )
    
    class Meta:
        model = Hotel
        fields = [
            'name',
            'location', 
            'description',
            'review_mark',
            'comments',
            'average_price',
            'photo_urls',
            'amenities'
        ]
    
    def create(self, validated_data):
        photo_urls = validated_data.pop('photo_urls', [])
        amenity_names = validated_data.pop('amenities', [])
        
        hotel = Hotel.objects.create(**validated_data)
        
        for url in photo_urls:
            HotelPhoto.objects.create(hotel=hotel, url=url)
        
        amenity_objects = []
        for name in amenity_names:
            amenity, created = Amenity.objects.get_or_create(name=name)
            amenity_objects.append(amenity)
        
        hotel.amenities.set(amenity_objects)
        
        return hotel