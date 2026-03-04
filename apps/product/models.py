from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator,
    MinLengthValidator,
    MaxLengthValidator
)
from decimal import Decimal
from apps.category.models import Category


class Product(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_user")
	name = models.CharField(
	    validators=[MinLengthValidator(10), MaxLengthValidator(255)],
	    db_index=True
	)
	description = models.TextField(validators=[MaxLengthValidator(1000)])
	price = models.DecimalField(
	    max_digits=10,
	    decimal_places=2,
	    validators=[MinValueValidator(Decimal("0.00"))]
	)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Продукт"
		verbose_name_plural = "Продукты"
		ordering = ["-created_at"]
		indexes = [models.Index(fields=["name", "description"])]
	
	def __str__(self):
		return f"<Product(id={self.id}, name={self.name})>"
	
	@property
	def is_expensive(self):
		return self.price > Decimal("100.00")
	
	def clean(self):
		try:
			price = float(self.price)
			print(price)
			if int(self.price) < 0:
				raise ValidationError({"price": "Цена не может быть отрицательной"})
		except (ValueError, TypeError):
			raise ValidationError({"price": "Введите корректную цену"})
	
	def deactivate(self):
		self.is_active = False
		self.save(update_fields=["is_active"])
	
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
	image = models.ImageField(upload_to="product_images/")
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"<ProductImage(id={self.id}, product={self.product.name})>"
	
