from django.db import models


class EmailVerification(models.Model):
	email = models.EmailField(db_index=True)
	code = models.IntegerField()
	is_verifed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name = "EmailVerification"
		verbose_name_plural = "EmailVerifications"
		indexes = [models.Index(fields=["email"])]
		ordering = ["-created_at"]
	
	def __str__(self):
		return f"<EmailVerification(id={self.id})>"

