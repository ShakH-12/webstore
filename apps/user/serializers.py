from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmailVerification


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
		if User.objects.filter(email=attrs["email"]).exists():
			raise serializers.ValidationError({"email": "email already taked"})
		return attrs
	
	def create(self, validated_data):
		validated_data.pop("password2")
		user = User.objects.create_user(**validated_data)
		user.is_active = False
		user.save()
		return user


class ResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username"]


class ResponseEmailVerificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmailVerification
		fields = "__all__"


class CreateEmailVerificationSerializer(serializers.ModelSerializer):
	email = serializers.CharField()
	code = serializers.IntegerField()
	
	class Meta:
		model = EmailVerification
		fields = ["email", "code"]
	
	def validate(self, attrs):
		return attrs
	
	def create(self, validated_data):
		ev = EmailVerification.objects.create(**validated_data)
		return ev
