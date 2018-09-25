import requests

from pybricks.groups import GroupsApi
from pybricks.jobs import JobsApi
from pybricks.scim import ScimApi
from pybricks.secrets import SecretsApi
from pybricks.workspace import WorkspaceApi


class PyBricksClient(object):
    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}
        self._workspace = WorkspaceApi(hostname, token)
        self._jobs = JobsApi(hostname, token)
        self._groups = GroupsApi(hostname, token)
        self._scim = ScimApi(hostname, token)
        self._secrets = SecretsApi(hostname, token)

    @property
    def workspace(self):
        """The workspace api"""
        return self._workspace

    @property
    def jobs(self):
        """The jobs api"""
        return self._jobs

    @property
    def groups(self):
        """The groups api"""
        return self._groups

    @property
    def scim(self):
        """The scim api"""
        return self._scim

    @property
    def secrets(self):
        """The secrets api"""
        return self._secrets

    def get_users(self):
        endpoint = "2.0/workspace/list"
        result = set()
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': '/Users'}
        req = requests.get(url, params=params, headers=self.__headers)

        objects = req.json()['objects']
        for user in objects:
            alias = user['path'].split('/')[2]
            result.add(alias)

        return result

    def user_exists(self, user_name):
        return user_name in self.get_users()