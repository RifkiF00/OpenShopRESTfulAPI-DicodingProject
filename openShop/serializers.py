from rest_framework import serializers
from rest_framework.reverse import reverse
from openShop.models import Product

class ProductSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'shop', 'price', 'sku', 'description', 
            'location', 'discount', 'category', 'stock', 
            'is_available', 'picture', 'is_delete', '_links'
        ]
        
    def get__links(self, obj):
        request = self.context.get('request')
        
        # We need the base URL for the list endpoint
        try:
            base_url = reverse('product-list', request=request)
        except:
            base_url = '/products/'
            
        try:
            detail_url = reverse('product-detail', kwargs={'pk': obj.pk}, request=request)
        except:
            detail_url = f'/products/{obj.pk}/'
            
        return [
            {
                "rel": "self",
                "href": base_url,
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": detail_url,
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": detail_url,
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": detail_url,
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]