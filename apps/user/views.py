from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response

from .models import EmailVerification
from .serializers import RegisterSerializer, ResponseSerializer, CreateEmailVerificationSerializer
import random


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		user = ResponseSerializer(serializer.save()).data
		code = random.randint(10000, 99999)
		ve = EmailVerification.objects.create(code=code, email=request.data.get("email"))
		
		return Response({"user": user, "verification_id": ve.id})


class VerifyEmail(generics.views.APIView):
	queryset = User.objects.all()
	serializer_class = CreateEmailVerificationSerializer
	
	def post(self, request):
		verification_id = request.data.get("verification_id")
		code = request.data.get("code")
		
		if not all([verification_id, code]):
			return Response({"error": "verification_id and code are required"}, status=400)
		
		verification = EmailVerification.objects.filter(id=verification_id).first()
		if not verification:
			return Response({"error": "verification not found"}, status=404)
		
		user = User.objects.filter(email=verification.email).first()
		if not user:
			return Response({"error": "user not found"}, status=404)
		
		if code != verification.code:
			return Response({"error": "code didn't match"}, status=400)
		
		user.is_active = True
		verification.is_verifed = True
		user.save()
		verification.save()
		return Response(ResponseSerializer(user).data)
		