import json
import os

import requests


class PyBricksClient(object):
    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

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

    def get_users_v2(self):
        endpoint = "2.0/preview/scim/v2/Users"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()
        return objects

    def user_exists(self, user_name):
        return user_name in self.get_users()

    def get_groups(self):
        endpoint = "2.0/groups/list"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()['group_names']
        return objects

    def get_group_members(self, group_name):
        endpoint = "2.0/groups/list-members"
        params = {'group_name': group_name}
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()['members']
        return objects

    def group_exists(self, group_name):
        return group_name in self.get_groups()

    def create_group(self, group_name):
        endpoint = "2.0/groups/create"
        data = json.dumps({'group_name': group_name})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def delete_group(self, group_name):
        endpoint = "2.0/groups/delete"
        data = json.dumps({'group_name': group_name})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def add_member_to_group(self, user_or_group, group_name):
        endpoint = "2.0/groups/add-member"
        member_type = None

        if self.user_exists(user_or_group):
            member_type = 'user_name'
        elif self.group_exists(user_or_group):
            member_type = 'group_name'

        if member_type:
            data = json.dumps({member_type: user_or_group, 'parent_name': group_name})
            url = "%s%s" % (self.hostname, endpoint)
            req = requests.post(url, headers=self.__headers, data=data)
            objects = req.json()
            return objects

    def remove_member_from_group(self, user_or_group, group_name):
        endpoint = "2.0/groups/remove-member"
        member_type = None

        if self.user_exists(user_or_group):
            member_type = 'user_name'
        elif self.group_exists(user_or_group):
            member_type = 'group_name'

        if member_type:
            data = json.dumps({member_type: user_or_group, 'parent_name': group_name})
            url = "%s%s" % (self.hostname, endpoint)
            req = requests.post(url, headers=self.__headers, data=data)
            objects = req.json()
            return objects

    def run_job_now(self, job_id, notebook_params):
        endpoint = "2.0/jobs/run-now"
        data = json.dumps({'job_id': job_id, 'notebook_params': notebook_params})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def get_secret_scopes(self):
        endpoint = "2.0/secrets/scopes/list"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()
        return objects

    def create_secret_scope(self, scope, initial_manage_principal="users"):
        endpoint = "2.0/secrets/scopes/create"
        data = json.dumps({'scope': scope, 'initial_manage_principal': initial_manage_principal})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def get_secrets(self, scope):
        endpoint = "2.0/secrets/list"
        params = {'scope': scope}
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()['secrets']
        return objects

    def add_secret(self, scope, key, string_value):
        endpoint = "2.0/secrets/put"
        data = json.dumps({'scope': scope, 'key': key, 'string_value': string_value})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def list_workspace(self, path, recursive=False):
        endpoint = "2.0/workspace/list"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path}
        req = requests.get(url, params=params, headers=self.__headers)
        response = req.json()
        if len(response) > 0:
            objects = response['objects']
            if not recursive:
                return objects
            else:
                for element in objects:
                    yield element
                    if element['object_type'] == 'DIRECTORY':
                        yield from self.list_workspace(element['path'], recursive)

    def get_workspace_status(self, path):
        endpoint = "2.0/workspace/get-status"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path}
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects

    def import_workspace(self, content, path, language, path_format="SOURCE", overwrite=True):
        endpoint = "2.0/workspace/import"
        url = "%s%s" % (self.hostname, endpoint)
        filepath = os.path.dirname(path)
        self.mkdirs_workspace(filepath)

        data = json.dumps(
            {'content': content, 'path': path, 'language': language, 'overwrite': overwrite, 'format': path_format})
        req = requests.post(url, headers=self.__headers, data=data)

        objects = req.json()
        return objects

    def export_workspace(self, path, path_format):
        endpoint = "2.0/workspace/export"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path, 'format': path_format}
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects

    def mkdirs_workspace(self, path):
        endpoint = "2.0/workspace/mkdirs"
        url = "%s%s" % (self.hostname, endpoint)
        data = json.dumps({'path': path})
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def delete_workspace(self, path, recursive=False):
        endpoint = "2.0/workspace/delete"
        url = "%s%s" % (self.hostname, endpoint)
        data = json.dumps({'path': path, 'recursive': recursive})
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects
