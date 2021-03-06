from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.urls import reverse

from .models import *
from .calculations import *
from .check_data import *

import csv
import os
from pathlib import Path
import logging

# Create your views here.

BASE_DIR     = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL    = '/media/'
MEDIA_ROOT   = os.path.join(BASE_DIR, 'media')
results_path = os.path.join(MEDIA_ROOT,"results.csv")
logger       = logging.getLogger(__name__)

def index(request):
    return render(request, "tech/index.html",{
        "models":MlModel.objects.all()
    })

def select_model(request):
    if request.method  =="POST":
        try:
            code           = request.POST["selected_model"]
            model          = MlModel.objects.get(code=code)
            selected_model = selectedModel(code=model.code, mdl=model.mdl)
            selected_model.save()
        except Exception as e:
            #DBで何か変なことが起きていたらログを記録してもう一度入力させる
            logger.error(e)
            return render(request, "tech/index.html" ,{
            "models":MlModel.objects.all()
        })
        if "NN" in code:
            return render(request,"tech/make_NN_model.html")
        else:
            return HttpResponseRedirect(reverse("datas"))
    else:
        return render(request, "tech/index.html" ,{
            "models":MlModel.objects.all()
        })

def make_NN(request):
    #もしもDBが動いて無い場合の処理を記述する?
    if request.method=="POST":
        model          = NN_layers(layer1=request.POST["layer1"],layer2=request.POST["layer2"] )
        model.save()
        return HttpResponseRedirect(reverse("datas"))
    else:
        return HttpResponseRedirect(reverse("empty"))


def select_data(request):
    """
    POSTされたデータがcsvか判定し、calculation に渡す
    """
    if request.method =="POST":
        form          = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #data is save to /media
            form.save()
            return HttpResponseRedirect(reverse("calculation"))
        else:   
            dataform      = UploadFileForm        
            return render(request, "tech/select_data.html",{
                "msg" : form.errors["data"],
                "form": dataform
            })
    else:
        dataform      = UploadFileForm
        return render(request, "tech/select_data.html",{
                "form":dataform,

                })
    
def calculation(request):
    """
    GETの時は、selectedData とselectedModel に値が格納されている時だけ、確認画面に行く
    POSTの時は、計算結果をmodelに格納してget_resultに飛ぶ
    """
    if selectedModel.objects.exists() and selectedData.objects.exists() :
        # modelとdataが選ばれていたときにcalculationsから機械学習モデルを動かす
        if not request.method == "POST":
            return render(request, "tech/calculation.html",{
                "data"  : selectedData.objects.last(),
                "model" : selectedModel.objects.last()
            })
        else:
            #selected_mdl に選択されたモデルの情報を渡す
            global selected_mdl
            mlmodel = selectedModel.objects.last().code
            if "NN" in mlmodel: 
                layers       = NN_layers.objects.last()
                layers       = (layers.layer1, layers.layer2)
                selected_mdl = eval(mlmodel)(data=selectedData.objects.last().data,layers=layers )
            else:
                selected_mdl = eval(mlmodel)(data=selectedData.objects.last().data )
            #model にあったデータの形かチェックする。yの値が変な時はabonが出てくる
            data_type = selected_mdl.y.dtype
            if "regression" in mlmodel.lower():
                if check_data_type(model="regression", data_type=data_type) == "abon":
                    return render(request, "tech/error.html",{
                        "msg": "回帰の時は、A列に実数か整数を使用してください"
                    })
                else:
                    pass
            if "classification" in mlmodel.lower():
                if check_data_type(model="classification", data_type=data_type) == "abon":
                    return render(request, "tech/error.html",{
                        "msg": "分類の時は、A列に整数か文字を使用してください"
                    })
                else:
                    pass
            selected_mdl.learning()
            return render(request, "tech/get_result.html",{
            "results": results.objects.last()
        }) 
            
    else:
        return HttpResponseRedirect(reverse("empty"))

def get_result(request):
    """
    result.html から request が飛んできたらモデルに保存してあるlossの値を表示する
    result.html から request がgetで飛んで来たら、caluculations.py のresults を動かして結果を作成し、ダウンロードさせる 
    """
    if request.method =="POST":
        if "selected_mdl" in globals():
            response                        = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="results.csv"'
            #selected_mdl が定義されていないことになる事があるのは何故？
            output                          = selected_mdl.get_results()
            length_of_results               = len(output)
            writer                          = csv.writer(response)
            #columns の出力
            writer.writerow(output.columns)
            #結果の出力
            for i in range(length_of_results):
                writer.writerow(output.iloc[i,:])
            return response
        else:
            messages.error(request, "エラーが出ています。条件を確認してもう一度計算してください。")
            return render(request, "tech/calculation.html")
        
    else:
        return render(request, "tech/get_result.html",{
            "results": results
        })

def help(request):
    """
    help ページからモデルが選ばれていたら、そのモデルの説明ページへ飛ばす(ブログ)
    """
    if request.method =="POST":
        masamune      = "https://masamunetogetoge.com/"
        overview      = "-overview"
        content       = request.POST["help_content"].lower()
        if "nn" in content:
            content ="nn"
        guide_path    = masamune + content + overview
        return HttpResponseRedirect(guide_path)   
    else:
        return render(request, "tech/help.html",{
            "models":MlModel.objects.all(),
        })
def empty(request):
    return render(request,"tech/empty.html" )

def error(request):
    return render(request,"tech/error.html" )
