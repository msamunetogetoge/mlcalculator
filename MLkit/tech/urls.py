from django.urls import path

from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("select_model", views.select_model, name="model"),
    path("get_result", views.get_result, name="result"),
    

]