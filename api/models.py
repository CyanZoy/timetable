from django.db import models


class Appid(models.Model):
    appid = models.CharField(max_length=255, primary_key=True)
    appsecret = models.CharField(max_length=255)

    class Meta:
        db_table = 'auth_appid'
