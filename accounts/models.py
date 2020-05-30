from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# class accountCode(models.Model):
# 	# user profile
# 	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

# 	# turn true if user is connected with telegram
# 	user_connected = models.BooleanField(default=False)

# 	# randomly generated code
# 	verify_code = models.CharField(max_length=10, unique=True, default=''.join(random.choice(string.ascii_letters) for i in range(10)))

# 	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

# 	def __str__(self):
# 		return f'{self.user} {self.verify_code} - {self.user_connected}'

# 	class Meta:
# 		ordering = ["-timestamp", "-updated"]



# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	phone_number = models.CharField(max_length=12, blank=True)
# 	bio = models.TextField(max_length=500, blank=True)

# 	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
# 	instance.profile.save()