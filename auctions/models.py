from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=2000)
    starting_bid = models.FloatField()
    image = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=32, null=True, blank=True)

class create_listing:
    title = None
    description = None
    starting_bid = None

    def __init__(self, title, description, starting_bid, image = None):
        
        self.title = title
        self.description = description
        self.starting_bid = starting_bid
        self.image = image

    def validate_items(self):
        if self.title:
            pass
        if self.description:
            pass
        if self.starting_bid:
            pass

    

        
    
        
