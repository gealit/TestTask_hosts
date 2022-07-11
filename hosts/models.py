from django.contrib.auth.models import User
from django.db import models


class Host(models.Model):
    class Resource(models.TextChoices):
        win = '1', 'windows'
        unx = '2', 'unix'
        sql = '3', 'sql'

    users = models.ManyToManyField(User)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    resource = models.CharField(
        max_length=3,
        choices=Resource.choices,
        default=Resource.win
    )
    time_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-time_update',)

    def __str__(self):
        return f'Host: {self.ip_address}:{self.port}'
