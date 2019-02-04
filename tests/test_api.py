# -*- coding: utf-8 -*-

from datetime import datetime

from flexmock import flexmock
import json

from . import assert_redirects, TestCase

prescription = {
	"prescription": [
		["PARACETAMOL", 4, 35],
		["VARFARINA", 1, 20],
		["VANCOMICINA", 1, 15],
		["MEROPENEN", 0]
	]
}

wrong_prescription = {
	"prescccription": []
}

class TestScore(TestCase):
	def test_empty_json(self):
		response = self.client.post('/score')
		assert response.status_code == 406

	def test_complete_json(self):
		response = self.client.post('/score', content_type='application/json', data=json.dumps(prescription))
		assert response.status_code == 200

	def test_wrong_json(self):
		response = self.client.post('/score', content_type='application/json', data=json.dumps(wrong_prescription))
		assert response.status_code == 406