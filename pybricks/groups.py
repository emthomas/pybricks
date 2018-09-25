import json
import os

import requests


class GroupsApi(object):
    """The Groups API"""

    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

    def list(self):
        """Returns all of the groups in an organization."""

        endpoint = "2.0/groups/list"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()['group_names']
        return objects

    def get_members(self, group_name):
        """Returns all of the members of a particular group."""

        endpoint = "2.0/groups/list-members"
        params = {'group_name': group_name}
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()['members']
        return objects

    def exists(self, group_name):
        """Returns true if the group exists. False otherwise"""
        return group_name in self.list()

    def create(self, group_name):
        """Creates a new group with the given name."""

        endpoint = "2.0/groups/create"
        data = json.dumps({'group_name': group_name})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def delete(self, group_name):
        """Removes a group from this organization."""

        endpoint = "2.0/groups/delete"
        data = json.dumps({'group_name': group_name})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def add_member(self, user_or_group, group_name):
        """Adds a user or group to a group."""

        endpoint = "2.0/groups/add-member"
        member_type = None

        if self.user_exists(user_or_group):
            member_type = 'user_name'
        elif self.exists(user_or_group):
            member_type = 'group_name'

        if member_type:
            data = json.dumps({member_type: user_or_group, 'parent_name': group_name})
            url = "%s%s" % (self.hostname, endpoint)
            req = requests.post(url, headers=self.__headers, data=data)
            objects = req.json()
            return objects

    def remove_member(self, user_or_group, group_name):
        """Removes a user or group from a group."""

        endpoint = "2.0/groups/remove-member"
        member_type = None

        if self.user_exists(user_or_group):
            member_type = 'user_name'
        elif self.exists(user_or_group):
            member_type = 'group_name'

        if member_type:
            data = json.dumps({member_type: user_or_group, 'parent_name': group_name})
            url = "%s%s" % (self.hostname, endpoint)
            req = requests.post(url, headers=self.__headers, data=data)
            objects = req.json()
            return objects
