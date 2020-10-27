import os
from django.db import models
from django import forms
from django.forms import ModelForm

from django.core.validators import FileExtensionValidator

# Create your models here.

class MlModel(models.Model):
    mdl         = models.CharField(max_length=64)
    code        = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.mdl} :({self.code})"

class selectedModel(models.Model):
    mdl         = models.CharField(max_length=64)
    code        = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.mdl} :({self.code})"

class NN_layers(models.Model):
    layer1      = models.PositiveSmallIntegerField(default=64)
    layer2      = models.PositiveSmallIntegerField(default=64)
    def __str__(self):
        return f"Layer1: {self.layer1}, Layer2:{self.layer2}"


class selectedData(models.Model):
    title       = models.CharField('title', max_length=64)
    data        = models.FileField(upload_to="media",null=True, 
                  validators=[FileExtensionValidator(".csv", "csvファイル以外は使えません。すみません。")])

    def __str__(self):
        return self.title

class UploadFileForm(ModelForm):

    class Meta:
        model    = selectedData 
        fields   = ('title','data' )

        

class results(models.Model):
    title        = models.CharField(max_length=64)
    loss_train   = models.CharField(max_length=10, default=0)
    loss_test    = models.CharField(max_length=10, default=0)
    description  = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title} :{self.loss_train}, {self.loss_test}: {self.description}"



    