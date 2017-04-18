# -*- coding: utf-8 -*-
"""
    rorocloud.client
    ~~~~~~~~~~~~~~~~

    This module provides the client interface to interact with the
    rorocloud service.

    :copyright: (c) 2017 by rorodata
    :license: Apache 2, see LICENSE for more details.
"""
import os
import requests

class Client(object):
    """The rorocloud client.
    """
    def __init__(self, base_url=None):
        self.base_url = base_url or get_rorocloud_default_url()
        self.auth = ("guest", "guest")

    def get(self, path):
        url = self.base_url.rstrip("/") + path
        return requests.get(url, auth=self.auth).json()

    def post(self, path, data):
        url = self.base_url.rstrip("/") + path
        return requests.post(url, json=data, auth=self.auth).json()

    def delete(self, path):
        url = self.base_url.rstrip("/") + path
        return requests.delete(url, auth=self.auth).json()

    def jobs(self):
        return [Job(job) for job in self.get("/jobs")]

    def get_job(self, job_id):
        path = "/jobs/" + job_id
        return Job(self.get(path))

    def get_logs(self, job_id):
        path = "/jobs/" + job_id + "/logs"
        return self.get(path)

    def stop_job(self, job_id):
        path = "/jobs/" + job_id
        self.delete(path)

    def run(self, command, shell=False):
        payload = {"command": list(command)}
        data = self.post("/jobs", payload)
        return Job(data)

class Job(object):
    def __init__(self, data):
        self.data = data
        self.id = data['jobid']
        self.command_args = data['details']['command']
        self.command = " ".join(self.command_args)

def get_rorocloud_default_url():
    return os.getenv("ROROCLOUD_URL") or "https://rorocloud.rorodata.com/"
