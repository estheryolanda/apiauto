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
        if len(response) == 0:
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
        """
        Get all tasks.
        :return:
        """
        response = RestClient().send_request("get", session=self.session,
                                             url=self.url_tasks, headers=HEADERS)
        if len(response["body"]) == 0:
            raise AssertionError("No tasks available")

        return response

    def delete_tasks(self, tasks_list):
        """
        Delete the tasks listed
        :param tasks_list: tasks id list
        :return:
        """
        for task in tasks_list:
            url = f"{self.url_tasks}/{task}"
            RestClient().send_request(method_name="delete", session=self.session, url=url, headers=HEADERS)

    def create_task(self, project_id=None, section_id=None):
        """
        Method to create a task
        :param project_id:
        :param section_id:
        :return:
        """
        data = {
            "content": "Task inside section",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        if project_id:
            data["project_id"] = project_id
        if section_id:
            data["section_id"] = section_id

        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_tasks, data=data)

        return response
