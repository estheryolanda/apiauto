"""
 This is a module for Projects using Node2
"""
import logging
import unittest
import requests
from nose2.tools import params

from config.config import TOKEN_TODO
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.INFO)


class Projects(unittest.TestCase):
    """
    Class to test the API for Projects
    """
    @classmethod
    def setUpClass(cls):
        """
        Setup Class only executed one time
        """
        print("Setup Class")
        cls.token = TOKEN_TODO

        print("Token from .env file: ", cls.token)
        cls.headers = {
            "Authorization": f"Bearer {cls.token}"
        }
        cls.url_base = "https://api.todoist.com/rest/v2/projects"

        # create project to be used in tests
        body_project = {
            "name": "Project 0"
        }
        response = requests.post(cls.url_base, headers=cls.headers, data=body_project, timeout=10)

        cls.project_id = response.json()["id"]
        cls.project_id_update = ""
        cls.projects_list = []

    def test_get_all_projects(self):
        """
        Test get all projects
        """
        response = requests.get(self.url_base, headers=self.headers, timeout=10)
        assert response.status_code == 200

    @params("Project 2", "1111111", "!@$$@$!@$")
    def test_create_project(self, name_project):
        """
        Test for create project
        """
        body_project = {
            "name": name_project
        }
        response = requests.post(self.url_base, headers=self.headers, data=body_project, timeout=10)
        LOGGER.info("Response for create project: %s", response.json())
        self.project_id_update = response.json()["id"]
        LOGGER.debug("Project id generated: %s", self.project_id_update)
        self.projects_list.append(self.project_id_update)
        assert response.status_code == 200

    def test_get_project(self):
        """
        Test get Project
        """
        url = f"{self.url_base}/{self.project_id}"
        response = requests.get(url, headers=self.headers, timeout=10)
        print(response.json())
        assert response.status_code == 200

    def test_delete_project(self):
        """
        Test delete a project
        """
        url = f"{self.url_base}/{self.project_id}"
        print(f"Test Delete: {self.project_id}")
        response = requests.delete(url, headers=self.headers,timeout=10)
        # validate project has been deleted
        assert response.status_code == 204

    def test_update_project(self):
        """
        Test to update a project.
        """
        url = f"{self.url_base}/{self.project_id_update}"
        data_update = {
            "name": "Project 2",
            "color": "red"
        }
        response = requests.post(url, headers=self.headers, data=data_update, timeout=10)
        print(response.json())
        assert response.status_code == 200

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        for project in cls.projects_list:
            url = f"{cls.url_base}/{project}"
            requests.delete(url, headers=cls.headers, timeout=10)
            LOGGER.info(f"Deleting project: {project}")
