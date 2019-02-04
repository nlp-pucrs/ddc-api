# -*- coding: utf-8 -*-

from datetime import datetime

from flexmock import flexmock

from . import assert_redirects, TestCase


class TestScoreEmpty(TestCase):
    def test_responds_to_score(self):
        response = self.client.post('/score')
        assert response.status_code == 406