# -*- coding: utf-8 -*-

from datetime import datetime

from flexmock import flexmock
import json

from . import assert_redirects, TestCase

class TestScore(TestCase):
	def test_get(self):
		response = self.client.post('/score')
		assert response.status_code == 405

	def test_empty_post(self):
		response = self.client.post('/score')
		assert response.status_code == 400

	def test_wrong_user(self):
		response = self.client.post('/score', data={'userid':'hospital10'})
		assert response.status_code == 401
