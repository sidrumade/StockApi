from django.db import models

# Create your models here.

class ApiKeys(models.Model):
    email = models.EmailField(max_length=30,null=True,blank=True)
    non_enc_key = models.CharField(max_length=50,default="", blank=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.non_enc_key
