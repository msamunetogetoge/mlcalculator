from django.db import models
from django.forms import ModelForm

# Create your models here.

class MlModel(models.Model):
    mdl         = models.CharField(max_length=64)
    code        = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.mdl} :({self.code})"

class selectedModel(models.Model):
    mdl         = models.CharField(max_length=64)
    code        = models.CharField(max_length=64)

class selectedData(models.Model):
    title       = models.CharField('title', max_length=64)
    data        = models.FileField(upload_to="media",null=True)

    def __str__(self):
        return self.title

class results(models.Model):
    title        = models.CharField(max_length=64)
    loss_train   = models.CharField(max_length=10, default=0)
    loss_test    = models.CharField(max_length=10, default=0)

    def __str__(self):
        return f"{self.title} :{self.loss_train}, {self.loss_test}"

class UploadFileForm(ModelForm):

    class Meta:
        model    = selectedData 
        fields   = ('title', 'data' )

    