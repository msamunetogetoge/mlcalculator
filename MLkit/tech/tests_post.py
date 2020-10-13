from django.test import Client, TestCase
from django.urls import reverse
from .models import *

import os
from pathlib import Path

import unittest
from unittest import mock
import logging

logger = logging.getLogger(__name__)

# Create your tests here.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

class MmlTestCase_post(TestCase):
	
	def setUp(self):
		m1             = MlModel.objects.create(mdl="回帰分析",code="Regression")  
		m2             = MlModel.objects.create(mdl="ロジスティック回帰",
		code="Logistic_Classification")
		m1.save()
		m2.save()
		data           = os.path.join(MEDIA_ROOT, "Davis.csv")
		title          = "Davis"
		selected_data  = selectedData(data=data, title=title)
		selected_data.save()
		selected_model = selectedModel(mdl=m1.mdl, code=m1.code)
		selected_model.save()
	
	def test_index(self):
		"""
		return render(request, "tech/index.html",{
        "models":MlModel.objects.all()
    	})
		"""
		c        = Client()
		response =  c.post("/tech/")
		self.assertEqual(response.status_code, 200)

	def test_calculation(self):
		"""
		model と正しいデータがある時、get_resultに遷移するかのテスト
		return HttpResponseRedirect(reverse("result")
		"""
		#setup
		c              = Client()
		m1             = MlModel.objects.create(mdl="回帰分析",code="Regression") 
		m1.save()
		data           = os.path.join(MEDIA_ROOT, "rensyu.csv")
		title          = "rensyu"
		selected_data  = selectedData(data=data, title=title)
		selected_data.save()
		selected_model = selectedModel(mdl=m1.mdl, code=m1.code)
		selected_model.save()
		#動作確認 
		#モデルを呼び出して動いているか、その結果を以てget_resultに飛んでいるか
		response       = c.post("/tech/calculation")
		self.assertEqual(response.status_code, 302)
			
	def test_empty(self):
		"""
		return render(request,"tech/empty.html" )
		"""
		c        = Client()
		response =  c.post("/tech/empty")
		self.assertEqual(response.status_code, 200)

	def test_error(self):
		"""
		return render(request,"tech/error.html" )
		"""
		c 		 = Client()
		response =  c.post("/tech/error")
		self.assertEqual(response.status_code, 200)
   
	def test_get_result1(self):
		"""
		calculation でモデルが計算された後、resultをダウンロードする時、正常に動作するかのテスト
		return response　;csv file 
		"""
		#setup
		c        = Client()
		m1       = MlModel.objects.create(mdl="回帰分析",code="Regression") 
		m1.save()
		data           = os.path.join(MEDIA_ROOT, "rensyu.csv")
		title          = "rensyu"
		selected_data  = selectedData(data=data, title=title)
		selected_data.save()
		selected_model = selectedModel(mdl=m1.mdl, code=m1.code)
		selected_model.save()
		response1 =  c.post("/tech/calculation")
		self.assertEqual(response1.status_code, 302)
		
		response2 = c.post("/tech/get_result")
		self.assertEqual(response2.status_code, 200)	

	def test_get_result2(self):
		"""
		calculation でモデルが計算されていない時、正常に動作するかのテスト
		return render(request, "tech/calculation.html") 
		"""
		#setup
		c        = Client()
		response = c.post("/tech/get_result")
		self.assertEqual(response.status_code, 200)
	
	def test_help(self):
		c			 = Client()
		help_content = {"help_content":"Regression"}
		response     =  c.post("/tech/help", help_content)
		self.assertEqual(response.status_code, 302)
	
	def test_make_NN(self):
		c        = Client()
		layers ={"layer1":64, "layer2":64}
		response =  c.post("/tech/make_NN_model",layers)
		self.assertEqual(response.status_code, 302)
	
	def test_select_data(self):
		c        = Client()
		response =  c.post("/tech/select_data")
		self.assertEqual(response.status_code, 302)

	def test_select_model_No_NN(self):
		"""
		NN model でないモデルが入力されたときの挙動
		return HttpResponseRedirect(reverse("datas"))
		"""
		c = Client()
		response = c.post(reverse("model"), data={"selected_model":MlModel.objects.last().code })
		self.assertEqual(response.status_code, 302)
	
	def test_select_model_NN(self):
		"""
		NN model が入力されたときの挙動
		return render(request,"tech/make_NN_model.html")
		"""
		c 		 = Client()
		m 		 = MlModel.objects.create(mdl="ニューラルネットワーク",code="NN_Regression") 
		m.save()
		response = c.post(reverse("model"), data={"selected_model":MlModel.objects.last().code })
		self.assertEqual(response.status_code, 200)

	
	def test_select_model_without_DB(self):
		"""
		selected_model = None の場合 
		try:
            code           = request.POST["selected_model"]
            model          = MlModel.objects.get(code=code)
            selected_model = selectedModel(code=model.code, mdl=model.mdl)
            selected_model.save()
        except Exception as e:
            #DBで何か変なことが起きていたらもう一度入力させる
            logger.error(e)
            return render(request, "tech/index.html" ,{
            "models":MlModel.objects.all()
        })
		"""

		c = Client()
		model = ""
		response = c.post(reverse("model"),data={"selected_model":model})
		
		self.assertEqual(response.status_code, 200)
		self.assertEqual(c.raise_request_exception, True )
		
		