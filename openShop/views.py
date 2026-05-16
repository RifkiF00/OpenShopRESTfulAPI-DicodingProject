from rest_framework import viewsets, status
from rest_framework.response import Response
from openShop.models import Product
from openShop.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Retrieve all if it's a detail request, else filter active
        if getattr(self, 'action', None) == 'retrieve':
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(is_delete=False)
            
        # Filter by name
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
            
        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
            
        return queryset
        
    def get_object(self):
        from django.http import Http404
        try:
            return super().get_object()
        except Http404:
            raise Http404("Not found.")
            
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"products": serializer.data})
        
    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()