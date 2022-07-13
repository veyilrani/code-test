from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Fact(models.Model):
    fact = RichTextField()
    like = models.IntegerField(null=True)
    user_id = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)



class Comments(models.Model):
    Comments = models.CharField(max_length=255)
    fact_id = models.IntegerField()

