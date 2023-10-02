import requests

from config.config import HEADERS
from utils.rest_client import RestClient
from utils.singleton import Singleton


class TodoBase(metaclass=Singleton):

    def __init__(self):
        self.url_projects = "https://api.todoist.com/rest/v2/projects"
        self.url_sections = "https://api.todoist.com/rest/v2/sections"
        self.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        self.session = requests.Session()

    def get_all_projects(self):
        """

        :return:
        """
        response = RestClient().send_request("get", session=self.session,
                                             url=self.url_projects, headers=HEADERS)
        if len(response.json()) == 0:
            raise AssertionError("No projects available")

        return response

    def create_project(self, name_project):
        body_project = {
            "name": name_project
        }
        response = RestClient().send_request("post", session=self.session, url=self.url_projects,
                                             headers=HEADERS, data=body_project)
        return response

    def delete_projects(self, projects_list):
        """
        Delete the projects listed
        :param projects_list:
        :return:
        """
        for project in projects_list:
            url = f"{self.url_projects}/{project}"
            RestClient().send_request(method_name="delete", session=self.session, url=url,
                                      headers=HEADERS)

    def get_all_sections(self):
        """
        get all sections.
        :return:
        """
        response = RestClient().send_request("get", session=self.session,
                                             url=self.url_sections, headers=HEADERS)
        if len(response) == 0:
            raise AssertionError("No sections available")

        return response

    def create_sections(self, section_names, project_id):
        """
        Test to create session
        :return:
        """
        section_id_list = []
        for name in section_names:
            data = {
                "project_id": project_id,
                "name": name
            }
            response = RestClient().send_request("post", session=self.session, headers=HEADERS, url=self.url_sections,
                                                 data=data)
            response_body = response["body"]
            section_id = response_body["id"]
            section_id_list.append(section_id)
        return section_id_list

    def get_all_tasks(self):
        response = RestClient().send_request("get", session=self.session,
                                             url=self.url_tasks, headers=HEADERS)
        if len(response.json()) == 0:
            raise AssertionError("No tasks available")

        return response


