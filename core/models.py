from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    app_name = "Blogs"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    # slug = models.SlugField(unique=True) # enable then when we need links
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=2200)
    detail = models.TextField(max_length=2200)

    publish = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("blogs:detail", kwargs={"slug" : self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

