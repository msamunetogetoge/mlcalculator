from django.contrib import admin

from .models import *
# Register your models here.

class TechniquwtAdmin(admin.ModelAdmin):
    list_display = ("id","mdl","code")

class SelectedModelAdmin(admin.ModelAdmin):
    list_display = ("id","mdl","code")

class SelectedDataAdmin(admin.ModelAdmin):
    list_display = ("id","title")

class ResultsAdmin(admin.ModelAdmin):
    list_display = ("id","title", "loss")

class LayersAdmin(admin.ModelAdmin):
    list_display = ("id","layer1", "layer2")

admin.site.register(MlModel)
admin.site.register(selectedModel)
admin.site.register(selectedData)
admin.site.register(results)
admin.site.register(NN_layers)