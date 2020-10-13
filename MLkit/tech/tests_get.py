from django.test import Client, TestCase

from .models import *

import os
from pathlib import Path
# Create your tests here.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
class MmlTestCase_get(TestCase):

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
		c        = Client()
		response =  c.get("/tech/")
		self.assertEqual(response.status_code, 200)

	def test_calculation(self):
		c        = Client()
		response =  c.get("/tech/calculation")
		self.assertEqual(response.status_code, 200)
	
	def test_empty(self):
		c        = Client()
		response =  c.get("/tech/empty")
		self.assertEqual(response.status_code, 200)

	def test_error(self):
		c        = Client()
		response =  c.get("/tech/error")
		self.assertEqual(response.status_code, 200)

	def test_get_result(self):
		c        = Client()
		response =  c.get("/tech/get_result")
		self.assertEqual(response.status_code, 200)

	def test_help(self):
		c        = Client()
		response =  c.get("/tech/help")
		self.assertEqual(response.status_code, 200)
	
	def test_make_NN(self):
		c        = Client()
		response =  c.get("/tech/make_NN_model")
		self.assertEqual(response.status_code, 302)
	
	def test_select_data(self):
		c        = Client()
		response =  c.get("/tech/select_data")
		self.assertEqual(response.status_code, 200)
	
