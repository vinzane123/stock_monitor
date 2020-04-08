from django.db import models
from django.contrib.auth.models import User

class ItemList(models.Model):
    user = models.ForeignKey(User,null=False,blank=False, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    item_name = models.TextField(null=False,blank=False)
    value = models.FloatField(null=True,blank=True,default=0)

    class Meta:
        ordering = ['created_on']
