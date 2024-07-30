from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models

User = get_user_model()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_page = models.URLField(validators=[URLValidator()], blank=True, null=True)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField (auto_now_add=True)

    def __str__(self):
        return str(self.pk)
