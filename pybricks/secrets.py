import json
import os

import requests


class SecretsApi(object):
    """The Secrets API"""

    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

    def scopes_list(self):
        """Lists all secret scopes available in the workspace."""

        endpoint = "2.0/secrets/scopes/list"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()
        return objects

    def create_scope(self, scope, initial_manage_principal="users"):
        """Creates a new secret scope."""

        endpoint = "2.0/secrets/scopes/create"
        data = json.dumps({'scope': scope, 'initial_manage_principal': initial_manage_principal})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def list(self, scope):
        """Lists the secret keys that are stored at this scope."""

        endpoint = "2.0/secrets/list"
        params = {'scope': scope}
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()['secrets']
        return objects

    def put(self, scope, key, string_value):
        endpoint = "2.0/secrets/put"
        data = json.dumps({'scope': scope, 'key': key, 'string_value': string_value})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects