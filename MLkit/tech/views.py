from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UploadFileForm
from .models import MlModel

import pandas as pd

# Create your views here.

def index(request):
    dataform = UploadFileForm()
    return render(request, "tech/index.html",{
        "form":dataform
    })



def select_model(request):
    if request.method =="POST":
        data=UploadFileForm(request.POST, request.FILES)

        if data.is_vaild():
            data=request.FILES["data"]
            data=pd.read_csv(data)

            return render(request, "tech/select_model.html",{
                "models":MlModel.objects.all(),
                #"data":data
            })
        else:
            return render(request, "tech/index.html")


def get_result(request):
    return render(request, "tech/get_result.html",{
        
    })