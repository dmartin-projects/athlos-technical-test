from django.db import models

    
class HotelPhoto(models.Model):
      hotel = models.ForeignKey("Hotel",
                                on_delete=models.CASCADE, 
                                related_name='photo_urls')
      url = models.URLField()

class Amenity(models.Model):
      name = models.CharField(max_length=100, unique=True)

      def __str__(self):
          return self.name
      
class Hotel(models.Model):

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    average_price = models.FloatField()
    description = models.TextField(blank=True,null=True)
    review_mark = models.FloatField()
    comments = models.IntegerField()
    amenities = models.ManyToManyField(Amenity, related_name='hotels', blank=True)

    def _str_(self):
        return f"{self.name}, {self.location}"