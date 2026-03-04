from django.contrib.auth.models import User
from rest_framework import serializers, permissions, parsers, generics
from rest_framework.response import Response

from apps.user.permissions import IsAdmin
from .permissions import IsOwner
from .models import Product, ProductImage
from .serializers import (
    CreateUpdateSerializer,
    ResponseSerializer
)


class ListCreateView(generics.ListCreateAPIView):
	queryset = Product.objects.all()
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
		images = request.FILES.getlist("images")
		if len(images) < 2:
			raise serializers.ValidationError({"images": "images must be more than 2"})
		
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		product = serializer.save(user=request.user)
		
		for image in images:
			ProductImage.objects.create(product=product, image=image)
		
		return Response(ResponseSerializer(product).data)


class RetrieveUpdateView(generics.RetrieveUpdateAPIView):
	queryset = Product.objects.all()
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
		instance = self.get_object()
		if instance.user != request.user:
			raise serializers.ValidationError({"error": "permission denied"})
		
		serializer = self.get_serializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		product = serializer.save()
		return Response(ResponseSerializer(product).data)
	

