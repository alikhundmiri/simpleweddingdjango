import random
import string
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# This class will create verification code for each telegram ID.
# using which the next class will associate a given chat_id with verify_code
class accountCode(models.Model):
	# user profile
	# user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	chat_id = models.CharField(max_length=20, blank=False)

	# randomly generated code
	verify_code = models.CharField(max_length=10, unique=True, default=''.join(random.choice(string.ascii_letters) for i in range(10)))

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return f'{self.chat_id} - {self.verify_code}'

	class Meta:
		ordering = ["-timestamp", "-updated"]


# This holds information such as 
# phone number
# bio
# chat_id which is a telegram id
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=12, blank=True, default=None, null=True)
	bio = models.TextField(max_length=500, blank=True)
	chat_id = models.CharField(max_length=20, blank=True)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return f'{self.user} - {self.chat_id}'

@receiver(post_save, sender=User, dispatch_uid='create_new_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
	print("in create_user_profile")
	if created:
		print("\n\ninstance ", instance)
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()