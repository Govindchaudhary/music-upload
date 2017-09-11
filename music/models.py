from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator


class Album(models.Model):
       user = models.ForeignKey(User, default=1)
       artist = models.CharField(max_length=250)
       album_title = models.CharField(max_length=500)
       genre = models.CharField(max_length=100)
       album_logo = models.FileField()
       is_favorite = models.BooleanField(default=False)
       slug            = models.SlugField(null=True, blank=True)

       def get_absolute_url(self):
             return reverse('music:detail',kwargs={'pk': self.slug})


       def __str__(self):
              return self.album_title + '-' +self.artist
       @property
       def title(self):
            return self.album_title
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    instance. album_title = instance. album_title.capitalize()
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
#     print('saved')
#     print(instance.timestamp)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#         instance.save()

pre_save.connect(rl_pre_save_receiver, sender=Album)

             

class Song(models.Model):

       album = models.ForeignKey(Album,on_delete=models.CASCADE,null=True)
       file_type = models.CharField(max_length=10)
       song_title = models.CharField(max_length=250)
       is_favorite = models.BooleanField(default = False)
       audio_file = models.FileField(null=True)
       def get_absolute_url(self):
             
             return reverse('music:detail',kwargs={'pk': self.album.slug})
       
       
       def __str__(self):
              return self.song_title 