from django.db import models
from users.models import User


class Visit(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor_visits')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_visits')
    in_time = models.DateTimeField(null=True)
    out_time = models.DateTimeField(null=True)
    purpose = models.CharField(max_length=100)
