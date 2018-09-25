import json
import os

import requests


class WorkspaceApi(object):
    """The Workspace API"""

    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

    def delete(self, path, recursive=False):
        """
        Deletes an object or a directory (and optionally recursively deletes all objects in the directory).

        If path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST.
        If path is a non-empty directory and recursive is set to false, this call returns an error DIRECTORY_NOT_EMPTY.
        Object deletion cannot be undone and deleting a directory recursively is not atomic.

        :param path: The absolute path of the notebook or directory. This field is required.
        :param recursive: The flag that specifies whether to delete the object recursively. It is false by default. Please note this deleting directory is not atomic. If it fails in the middle, some of objects under this directory may be deleted and cannot be undone.
        :return: Json response
        """
        endpoint = "2.0/workspace/delete"
        url = "%s%s" % (self.hostname, endpoint)
        data = json.dumps({'path': path, 'recursive': recursive})
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def export(self, path, path_format):
        """
        Exports a notebook or contents of an entire directory. If path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST. One can only export a directory in DBC format. If the exported data would exceed size limit, this call returns an error MAX_NOTEBOOK_SIZE_EXCEEDED. This API does not support exporting a library.

        :param path: The absolute path of the notebook or directory. Exporting directory is only support for DBC format. This field is required.
        :param path_format: This specifies the format of the exported file. By default, this is SOURCE. However it may be one of: SOURCE, HTML, JUPYTER, DBC. The value is case sensitive.
        :return:
        """
        endpoint = "2.0/workspace/export"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path, 'format': path_format}
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects

    def list(self, path, recursive=False):
        """
        Lists the contents of a directory, or the object if it is not a directory.
        If the input path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST

        :param path: The absolute path of the notebook or directory. This field is required.
        :param recursive: List recursively or not.
        :return: an iterator
        """
        endpoint = "2.0/workspace/list"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path}
        req = requests.get(url, params=params, headers=self.__headers)
        response = req.json()
        if len(response) > 0:
            objects = response['objects']
            if not recursive:
                for element in objects:
                    yield element
            else:
                for element in objects:
                    yield element
                    if element['object_type'] == 'DIRECTORY':
                        yield from self.list(element['path'], recursive)

    def get_status(self, path):
        """
        Gets the status of an object or a directory.
        If path does not exist, this call returns an error RESOURCE_DOES_NOT_EXIST.

        :param path: The absolute path of the notebook or directory. This field is required.
        :return: Json response
        """
        endpoint = "2.0/workspace/get-status"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'path': path}
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects

    def import_content(self, content, path, language, path_format="SOURCE", overwrite=True):
        """
        Imports a notebook or the contents of an entire directory.
        If path already exists and overwrite is set to false, this call returns an error RESOURCE_ALREADY_EXISTS.
        One can only use DBC format to import a directory

        :param content: The base64-encoded content. This has a limit of 10 MB.
        :param path: The absolute path of the notebook or directory. Importing directory is only support for DBC format. This field is required.
        :param language: The language. If format is set to SOURCE, this field is required; otherwise, it will be ignored
        :param path_format: This specifies the format of the file to be imported. By default, this is SOURCE. However it may be one of: SOURCE, HTML, JUPYTER, DBC. The value is case sensitive.
        :param overwrite: The flag that specifies whether to overwrite existing object. It is false by default.
        :return: JSON response
        """
        endpoint = "2.0/workspace/import"
        url = "%s%s" % (self.hostname, endpoint)
        filepath = os.path.dirname(path)
        self.mkdirs(filepath)

        data = json.dumps(
            {'content': content, 'path': path, 'language': language, 'overwrite': overwrite, 'format': path_format})
        req = requests.post(url, headers=self.__headers, data=data)

        objects = req.json()
        return objects

    def mkdirs(self, path):
        """Creates the given directory and necessary parent directories if they do not exists"""

        endpoint = "2.0/workspace/mkdirs"
        url = "%s%s" % (self.hostname, endpoint)
        data = json.dumps({'path': path})
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects
