from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response

from .serializers import RegisterSerializer, ResponseSerializer


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		user = serializer.save()
		return Response(ResponseSerializer(user).data)

