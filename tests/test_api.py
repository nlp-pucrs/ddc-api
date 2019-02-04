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
		str_response = response.data.decode('utf-8')
		json_obj = json.loads(str_response)
		assert json_obj['prescription'][0][3] != None
		assert json_obj['prescription'][2][3] == ""
		assert len(json_obj['prescription'][3]) == 3
		assert response.status_code == 200

	def test_wrong_json(self):
		response = self.client.post('/score', content_type='application/json', data=json.dumps(wrong_prescription))
		assert response.status_code == 406