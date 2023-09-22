import unittest
import requests
from nose2.tools import params


"""
Test for nose2
"""


class Projects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
                Setup Class only executed one time
        """
        print("Setup Class")
        cls.token = "98c44b35dde00a5f2df4ce7a675cc6e2d964f6a0"
        cls.headers = {
            "Authorization": "Bearer {}".format(cls.token)
        }
        cls.url_base = "https://api.todoist.com/rest/v2/projects"

        # create project  to used in test
        body_project ={
            "name": "Project 0"
        }
        response = requests.post(cls.url_base, headers=cls.headers, data=body_project)
        print(response.json())
        cls. project_id = response.json()["id"]
        cls.project_id_update = ""
        cls.project_list =[]

    def test_get_all_projects(self):
        """
        test for get all projects
        """
        # act
        response = requests.get(self.url_base, headers=self.headers)
        assert response.status_code == 200

    @params("Project2", "Project4", "Project3")
    def test_create_project(self, name_project):
        """
        test to verify creation of project
        """
        body_project = {
            "name": name_project
        }
        response = requests.post(self.url_base, headers=self.headers, data=body_project)
        print(response.json())
        self.project_id_update = response.json()["id"]
        self.project_list.append( self.project_id_update)
        assert response.status_code == 200

    def test_get_project(self):
        """
        Test get Project
        """
        url = f"{self.url_base}/{self.project_id}"
        response = requests.get(url, headers=self.headers)
        print(response.json())
        assert response.status_code == 200

    def test_update_project(self):
        url = f"{self.url_base}/{self.project_id_update}"

        data_update = {
            "name": "Project 2",
            "color": "red"
        }
        response = requests.post(url, headers=self.headers, data=data_update)
        print(response.json())
        assert response.status_code == 200

    def test_delete_project(self):
        url = f"{self.url_base}/{self.project_id}"
        response = requests.delete(url, headers=self.headers)
        # validate project has been deleted
        assert response.status_code == 204

    @classmethod
    def tearDownClass(cls):
        print("teardown Class")
        # delete projects
        for project in cls.project_list:
            url = f"{cls.url_base}/{project}"
            requests.delete(url, headers=cls.headers)
            print(f"Deleting project: {project}")
