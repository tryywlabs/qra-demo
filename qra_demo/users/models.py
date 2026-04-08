from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name