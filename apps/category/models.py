from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator
)


class Category(models.Model):
	name = models.CharField(
	    validators=[MinLengthValidator(5), MaxLengthValidator(50)],
	    db_index=True
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "Category"
		verbose_name_plural = "Categories"
		ordering = ["-created_at"]
		indexes = [models.Index(fields=["name"])]
	
	def __str__(self):
		return f"<Category(id={self.id}, name={self.name[:10]}...)>"
	
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


