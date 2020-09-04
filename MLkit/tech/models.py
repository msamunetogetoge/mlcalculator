from django.db import models

# Create your models here.

class MlModel(models.Model):
    mdl = models.CharField(max_length=64)
    code = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.mdl} :({self.code})"