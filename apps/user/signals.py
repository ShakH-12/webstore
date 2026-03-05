from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random


@receiver(post_save, sender=User)
def send_verify_code_email(sender, instance, created, **kwargs):
	"""
	
	"""

