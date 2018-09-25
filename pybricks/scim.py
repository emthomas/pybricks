import json
import os

import requests


class ScimApi(object):
    """The SCIM, or System for Cross-domain Identity Management API"""

    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

    def get_users(self):
        """Retrieve a list of all users in the Databricks workspace."""

        endpoint = "2.0/preview/scim/v2/Users"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()
        return objects
