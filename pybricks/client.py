import requests
import json


class PyBricksClient(object):
    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.headers = {'authorization': "Bearer %s" % token, "content-type": "application/json"}

    def get_users(self):
        endpoint = "2.0/workspace/list"
        result = set()
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': '/Users'}
        req = requests.get(url, params=params, headers=self.headers)

        objects = req.json()['objects']
        for user in objects:
            alias = user['path'].split('/')[2]
            result.add(alias)

        return result
