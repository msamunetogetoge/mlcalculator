from django.contrib import admin

from .models import MlModel
# Register your models here.

class TechniquwtAdmin(admin.ModelAdmin):
    list_display = ("id","mdl","code")

admin.site.register(MlModel)