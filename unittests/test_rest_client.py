import json
import logging
import unittest
from unittest.mock import Mock

import requests
from requests import Response

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestRestClient(unittest.TestCase):

    def setUp(self):
        self.rest_client = RestClient()
        self.session = requests.Session()


    def test_sent_request_sucess(self):
       response_mock =Mock(spec=Response)
       response_mock.status_code =200
       with patch.object(requests.Session, "get", return_value=reponse_mock) as mock_get:
           response = self.rest_client.send_request(method_name="get", session=self.session, url="https://google.com")
           mock_get.assert_called_once_with("https://google.com", headers='',data=None)
           self.assertEquals(response, response_mock)

    def test_send_request_post(self):
        response_mock = Mock(spec=Response)
        response_mock.status_code = 200
        body = {
            "key": "value"
        }
        with patch.object(requests.Session, "post", return_value=reponse_mock) as mock_get:
            response = self.rest_client.send_request(method_name="post", session=self.session,
                                                     url="https://google.com", data=json.dumps(body))
            mock_get.assert_called_once_with("https://google.com", headers='', data=json.dumps(body))
            self.assertEquals(response, response_mock)

    def test_send_request_invalid_method(self):
        with self.assertRaises(AssertionError):
            self.rest_client.send_request(method_name="put", session=self.session, url = "https://google.com")