from django.db import models
from django.conf import settings

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from core.utils import random_string_generator
from django.utils.text import Truncator

# Create your models here.
class catagories(models.Model):
    catagory_name = models.CharField(max_length=20)
    description = models.TextField(max_length=160)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.catagory_name

    # def get_absolute_url(self):
    #     return reverse("blogs:detail", kwargs={"slug" : self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]


def create_default_slug(title):
    return slugify((Truncator(title).chars(200) +'-'+ random_string_generator(size=4)))


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    # slug = models.SlugField(unique=True) # enable then when we need links
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=2200, blank=True)
    detail = models.TextField(max_length=2200)
    slug = models.SlugField(max_length=200, unique=True)
    # slug = models.AutoSlugField(null=True, default=None, unique=True, populate_from='title')
    catagory = models.ForeignKey(catagories, related_name='posts', default=1, on_delete=models.CASCADE)

    publish = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        """
        Slugify name if it doesn't exist. IMPORTANT: doesn't check to see
        if slug is a dupe!
        """
        if not self.slug:
            self.slug = create_default_slug(self.name)
        super(Post, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("article", kwargs={"slug" : self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

################   P R E    S A V E    S T U F F     F O R     S L U G     C R E A T I O N
def create_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify((Truncator(instance.title).chars(200) +'-'+ random_string_generator(size=4)))
    exists = Post.objects.filter(slug=slug).order_by("-id").exists()
    if exists:
        a = slug.split('-')
        a_list = a[:-1] #remove the last element from this list.
        slug = "-".join(a_list)        
        new_slug = "{slug}-{randstr}".format(slug=slug,randstr=random_string_generator(size=4))
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_jd_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_jd_receiver, sender=Post)