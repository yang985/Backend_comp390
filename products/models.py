from django.db import models
from django.db.models import JSONField
# Create your models here.


class Products(models.Model):
    owner = models.CharField(max_length =20,default='')
    ownerId = models.IntegerField(default='')
    componentData = JSONField()
    title = models.CharField(max_length =20,default='')
    desc = models.CharField(max_length =200,default='')
    hints = models.CharField(max_length=500,default='')
    label = models.CharField(max_length=10,default='')