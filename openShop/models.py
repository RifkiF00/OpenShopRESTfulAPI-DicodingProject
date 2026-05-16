from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    shop = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField()
    category = models.CharField(max_length=255)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    picture = models.URLField()
    is_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name