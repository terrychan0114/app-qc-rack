# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from server.models.status_info import StatusInfo  # noqa: E501
from server.test import BaseTestCase


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    def test_get_qcrack(self):
        """Test case for get_qcrack

        Get all status at Paterson
        """
        query_string = [('sorting', 'sorting_example')]
        response = self.client.open(
            '/status',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
