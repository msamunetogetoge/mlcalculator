from django.urls import path

from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("select_model", views.select_model, name="model"),
    path("select_data", views.select_data, name="datas"),
    path("get_result", views.get_result, name="result"),
    path("calculation", views.calculation, name="calculation"),

]