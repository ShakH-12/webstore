from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=8)
	password2 = serializers.CharField(write_only=True)
	email = serializers.EmailField()
	
	class Meta:
		model = User
		fields = ["username", "email", "password", "password2"]
	
	def validate(self, attrs):
		if attrs["password"] != attrs["password2"]:
			raise serializers.ValidationError({"password": "passwords didn't match"})
		return attrs
	
	def create(self, validated_data):
		validated_data.pop("password2")
		user = User.objects.create_user(**validated_data)
		return user


class ResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username"]

