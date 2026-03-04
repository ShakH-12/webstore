from rest_framework import permissions, generics
from rest_framework.response import Response

from apps.user.permissions import IsAdmin
from .models import Category
from .serializers import CategorySerializer


class ListCreateView(generics.ListCreateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	
	def get_permissions(self):
		if self.request.method == "POST":
			return [IsAdmin()]
		return [permissions.AllowAny()]


class RetrieveUpdateView(generics.RetrieveUpdateAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	
	def get_permissions(self):
		if self.request.method in ["PUT", "PATCH"]:
			return [IsAdmin()]
		return [permissions.AllowAny()]
