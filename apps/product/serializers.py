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
	
	def validate(self, attrs):
		images = self.context["request"].FILES.getlist("images")
		if len(images) < 2:
			raise serializers.ValidationError({"images": "At least 2 images are required."})
		return attrs
	
	def create(self, validated_data):
		images = self.context["request"].FILES.getlist("images")
		product = Product.objects.create(**validated_data)
		for image in images:
			ProductImage.objects.create(product=product, image=image)
		return product


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = "__all__"


class ResponseSerializer(serializers.ModelSerializer):
	product_images = ProductImageSerializer(required=False, many=True)
	class Meta:
		model = Product
		fields = "__all__"

	
