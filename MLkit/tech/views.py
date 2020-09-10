from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import MlModel, selectedModel, UploadFileForm, selectedData, results
from .calculations import Regression

import os
from pathlib import Path

# Create your views here.

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def index(request):
    dataform           = UploadFileForm()
    return render(request, "tech/index.html",{
            "form":dataform,
            })



def select_model(request):
    if request.method =="POST":
        code           = request.POST["selected_model"]
        model          = MlModel.objects.get(code=code)
        selected_model = selectedModel(code=model.code, mdl=model.mdl)
        selected_model.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tech/select_model.html" ,{
            "models":MlModel.objects.all()
        })
    


def select_data(request):
    if request.method =="POST":
        data          = UploadFileForm(request.POST, request.FILES)
        if data.is_valid():
            #data is save to /media
            data.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        dataform      = UploadFileForm()
        return render(request, "tech/select_data.html",{
                "form":dataform,

                })
    
def calculation(request):
    """
    selectedData とselectedModel に値が格納されている時だけ、確認画面に行く
    層でない時は、警告ページに飛ばすが、まだ作ってないのでindexに飛ばす
    """
    if selectedModel.objects.first() and selectedData.objects.first() :
        #計算ボタンからページに飛んだ時、modelとdataが選ばれていたら確認画面を表示する
        #計算ページのボタンからpost request が飛んできている時はRegression を動かす
        if not request.method == "POST":
            return render(request, "tech/calculation.html",{
                "data"  : selectedData.objects.first(),
                "model" : selectedModel.objects.first()
            })
        else:
            #RegressionモデルにselectedDataの値を渡して学習
            Regression(data=selectedData.objects.first().data ).learning()

            return HttpResponseRedirect(reverse("result"),{
                "results" : results.objects.all(),
            })
            
    else:
        return render(request, "tech/index.html")

def get_result(request):
    return render(request, "tech/get_result.html",{
        "results":results.objects.first()
    })
    pass
    """

    if request.method =="POST":
        data=UploadFileForm(request.POST, request.FILES)

        if data.is_vaild():
            data=request.FILES["data"]
            data=pd.read_csv(data)

            return render(request, "tech/get_result.html",{
                "models":MlModel.objects.all(),
                "data":data
            })
    else:
        return render(request, "tech/index.html")

    """
