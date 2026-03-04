from django.db.models import Prefetch
from rest_framework import serializers, permissions, parsers, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter

from .models import Product, ProductImage
from .serializers import (
    CreateUpdateSerializer,
    ResponseSerializer
)


class ListCreateView(generics.ListCreateAPIView):
	queryset = Product.objects.prefetch_related(Prefetch("product_images"))
	filter_backends = [SearchFilter]
	search_fields = ["name", "description"]
	parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
	
	def get_permissions(self):
		if self.request.method == "POST":
			return [permissions.IsAuthenticated()]
		return [permissions.AllowAny()]
	
	def get_serializer_class(self):
		if self.request.method == "POST":
			return CreateUpdateSerializer
		return ResponseSerializer
	
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		product = serializer.save(user=request.user)
		
		return Response(ResponseSerializer(product, context=self.get_serializer_context()).data, status=201)


class RetrieveUpdateView(generics.RetrieveUpdateAPIView):
	queryset = Product.objects.prefetch_related(Prefetch("product_images"))
	parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
	
	def get_permissions(self):
		if self.request.method in ["PUT", "PATCH"]:
			return [permissions.IsAuthenticated()]
		return [permissions.AllowAny()]
	
	def get_serializer_class(self):
		if self.request.method in ["PUT", "PATCH"]:
			return CreateUpdateSerializer
		return ResponseSerializer
	
	def update(self, request, *args, **kwargs):
		partial = kwargs.pop("partial", False)
		instance = self.get_object()
		if instance.user != request.user:
			raise PermissionDenied("You do not have permission to edit this product.")
				
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		product = serializer.save()
		return Response(ResponseSerializer(product, context=self.get_serializer_context()).data)
	

