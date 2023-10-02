import logging
import unittest

import requests

from api.todo_base import TodoBase
from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Tasks(unittest.TestCase):
    """
    Class  for tasks endpoint
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup Class only executed one time
        """
        cls.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        cls.session = requests.Session()
        cls.projects_list = []
        cls.tasks_list = []

    def test_create_task(self):
        """
        Test to create task
        :return:
        """
        response = TodoBase().create_task()
        self.tasks_list.append(response["body"]["id"])
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="task")

    def test_create_task_with_project_id(self):
        """
        Test to create a task with in a project
        :return:
        """
        project_created = TodoBase().create_project("Project Task")
        project_id = project_created["body"]["id"]
        response = TodoBase().create_task(project_id=project_id)
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="task")

    def test_create_task_with_section_id(self):
        """
        Test to create a task inside a section in a project.
        :return:
        """
        project_created = TodoBase().create_project("Project Task2")
        project_id = project_created["body"]["id"]
        section_id = TodoBase().create_sections(["section001"], project_id)
        response = TodoBase().create_task(section_id=section_id)
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="task")

    def test_get_all_tasks(self):
        """
        Test to get all tasks
        :return:
        """
        response = TodoBase().get_all_tasks()
        LOGGER.info("Number of tasks returned: %s", len(response["body"]))
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="tasks")

    def test_get_task_by_id(self):
        """
        Test to get a task by its id.
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS, url=url_task)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="task")

    def test_close_task(self):
        """
        Test to close a task.
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task Id to be closed: %s", task_id)
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_close)

        ValidateResponse().validate_response(actual_response=response, method="close", expected_status_code=204,
                                             feature="task")

    def test_reopen_task(self):
        """
        Test to close a task.
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task ID to be closed and reopen: %s", task_id)

        # close
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response_close = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                                   url=url_task_close)

        assert response_close["status"] == 204

        LOGGER.info("Task Id: %s", task_id)
        url_task_reopen = f"{self.url_tasks}/{task_id}/reopen"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_reopen)

        ValidateResponse().validate_response(actual_response=response, method="reopen", expected_status_code=204,
                                             feature="task")

    def test_update_task(self):
        """
        Test to update a task
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task ID to be updated: %s", task_id)
        self.tasks_list.append(task_id)

        response_update_task = self.update_task(task_id=task_id)
        ValidateResponse().validate_response(actual_response=response_update_task, method="post",
                                             expected_status_code=200, feature="task")

    def test_delete_task(self):
        """
        Test to delete a task.
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task Id be deleted: %s", task_id)

        # delete
        url_task_delete = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS, url=url_task_delete)

        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="task")

    def update_task(self, project_id=None, section_id=None, task_id=None):
        """
        Method to update a task
        :param project_id:
        :param section_id:
        :param task_id:
        :return:
        """
        data = {
            "content": "Task inside section Modified",
            "due_string": "tomorrow at 8:00",
            "due_lang": "en",
            "priority": 2
        }
        if project_id:
            data["project_id"] = project_id
        if section_id:
            data["section_id"] = section_id
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task, data=data)

        return response

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects and tasks created
        LOGGER.info("The following tasks will be deleted: %s", cls.tasks_list)
        TodoBase().delete_projects(cls.projects_list)
        TodoBase().delete_tasks(cls.tasks_list)
