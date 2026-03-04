from rest_framework import serializers
from .models import Product, ProductImage


class CreateUpdateSerializer(serializers.ModelSerializer):
	name = serializers.CharField(min_length=10, max_length=255)
	description = serializers.CharField(min_length=10, max_length=1000)
	price = serializers.CharField()
	
	class Meta:
		model = Product
		fields = ["user", "name", "description", "price"]
		read_only_fields = ["user"]
	
	def create(self, validated_data):
		product = Product.objects.create(**validated_data)
		return product


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
	product_images = ProductImageSerializer(many=True)
	class Meta:
		model = Product
		fields = "__all__"

	
