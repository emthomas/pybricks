import json
import os

import requests


class JobsApi(object):
    """The Jobs API"""

    def __init__(self, hostname, token):
        self.hostname = "%s/api/" % hostname
        self.__headers = {'authorization': "Bearer %s" % token, "content-type": "application/scim+json",
                          "accept": "application/scim+json"}

    def run_now(self, job_id, notebook_params):
        """
        Runs the job now, and returns the run_id of the triggered run.

        :param job_id: The job id INT number
        :param notebook_params: A map from keys to values for jobs with notebook task, e.g. "notebook_params": {"name": "john doe", "age":  "35"}
        :return:
        """

        endpoint = "2.0/jobs/run-now"
        data = json.dumps({'job_id': job_id, 'notebook_params': notebook_params})
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.post(url, headers=self.__headers, data=data)
        objects = req.json()
        return objects

    def get(self, job_id):
        """Retrieves information about a single job."""

        endpoint = "2.0/jobs/get"
        params = {'job_id': job_id}
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects

    def list(self):
        """Lists all jobs."""

        endpoint = "2.0/jobs/list"
        url = "%s%s" % (self.hostname, endpoint)
        req = requests.get(url, headers=self.__headers)
        objects = req.json()['jobs']
        return objects

    def get_by_name(self, job_name):
        """Retrieves information about a single job by name."""

        for job in self.list():
            if job['settings']['name'] == job_name:
                return self.get(int(job['job_id']))

    def runs_list(self, job_id, active_only=True):
        """Lists runs from most recently started to least."""

        endpoint = "2.0/jobs/runs/list"
        url = "%s%s" % (self.hostname, endpoint)
        params = {'job_id': job_id, 'active_only': active_only}
        req = requests.get(url, headers=self.__headers, params=params)
        objects = req.json()
        return objects
