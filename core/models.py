from django.db import models
from django.conf import settings

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

from core.utils import random_string_generator
from django.utils.text import Truncator


class quran(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    slug = models.CharField(max_length=10, unique=True)
    # a counter to see how many times each aiyath is requested
    request = models.IntegerField(default=0)
    
    # aiyath number. surah 2 and aiyath 1 will be 8. because surah fatiha has 7 aiyath
    aiyath_number = models.IntegerField() #<- use this to get quran audio url
    
    # quran aiyath
    text = models.CharField(max_length=7000) #<= the longest aiyah (2:282) is 1200 char long in arabic. and 6300 long in byte text. not sure which willbe used to share here 
    
    # quran audio
    audio_64 = models.CharField(max_length=100)
    audio_128 = models.CharField(max_length=100)

    surah_number = models.IntegerField()
    surah_name = models.CharField(max_length=200)
    surah_englishName = models.CharField(max_length=100)
    surah_englishNameTranslation = models.CharField(max_length=500)
    surah_numberOfAyahs = models.IntegerField() 
    surah_revelationType = models.CharField(max_length=100)

    # aiyath number
    numberInSurah = models.IntegerField()
    juz = models.IntegerField()
    manzil = models.IntegerField()
    page = models.IntegerField()
    ruku = models.IntegerField()
    hizbQuarter = models.IntegerField()
    sajda = models.BooleanField(default=False)

    def __str__(self):
        return str(self.surah_englishName) + ":" + str(self.numberInSurah)

    def save(self, *args, **kwargs):
        self.slug = str(self.surah_number) +"-"+ str(self.numberInSurah)
        super(quran, self).save(*args, **kwargs) # Call the "real" save() method.

    def existing_slug(self, *args, **kwargs):
        return str(self.surah_number) +":"+ str(self.numberInSurah)
    # def get_absolute_url(self):
    #     return reverse("blogs:detail", kwargs={"slug" : self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]
        # unique_together = ('surah_number', 'numberInSurah')        

# Create your models here.
default_meta_description = 'Please enter meta description for better visibility'
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
    detail = models.TextField(max_length=22000)
    meta_description = models.TextField(max_length=160, default=default_meta_description)
    slug = models.SlugField(max_length=200, unique=True)
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
            self.slug = create_default_slug(self.title)
        super(Post, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("core:article", kwargs={"slug" : self.slug})

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