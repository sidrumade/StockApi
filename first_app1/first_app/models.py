from django.db import models


class ApiKeys(models.Model):
    non_enc_key = models.CharField(default="", blank=True)
    enc_key = models.CharField(default="", blank=True)
    active=models.BooleanField(default=False)

    def __str__(self):
        return self.non_enc_key
