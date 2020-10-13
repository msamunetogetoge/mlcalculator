import os
from pathlib import Path

from django.urls import path

from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("empty", views.empty, name="empty"),
    path("select_model", views.select_model, name="model"),
    path("make_NN_model", views.make_NN, name="make_NN"),
    path("select_data", views.select_data, name="datas"),
    path("get_result", views.get_result, name="result"),
    path("calculation", views.calculation, name="calculation"),
    path("help", views.help, name="help"),
    path("error", views.error, name="error"),

]
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')