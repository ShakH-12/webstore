from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
	name = serializers.CharField(min_length=5, max_length=24)
	class Meta:
		model = Category
		fields = ["name", "created_at", "updated_at"]
		read_only_fields = []
	
	def create(self, data):
		category = Category.objects.create(**data)
		return category


