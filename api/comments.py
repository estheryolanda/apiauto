import logging
import unittest

import requests

from api.todo_base import TodoBase
from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Comments(unittest.TestCase):
    """
    Class for Comments endpoint
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup Class only executed one time
        """
        cls.url_comments = "https://api.todoist.com/rest/v2/comments"
        cls.session = requests.Session()
        cls.projects_list = []
        cls.tasks_list = []

    def test_create_comment_for_project(self):
        """
        Test to comment task
        :return:
        """
        project_created = TodoBase().create_project("Project with comments")
        project_id = project_created["body"]["id"]
        LOGGER.info("Project ID be where the comment will be created: %s", project_id)
        response = self.create_comment(project_id=project_id, content="Need one bottle of milk")
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="comment")

    def test_create_comment_for_task(self):
        """
        Test to comment task
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        LOGGER.info("Task Id where the comment will be created: %s", task_id)
        response = self.create_comment(task_id=task_id, content="Need some apples")
        self.tasks_list.append(task_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="comment")

    def test_get_comment(self):
        """
        Test get a comment
        :return:
        """
        response_create_task = TodoBase().create_task()
        task_id = response_create_task["body"]["id"]
        self.tasks_list.append(task_id)
        LOGGER.info("Task Id where the comment will be created: %s", task_id)
        response = self.create_comment(task_id=task_id, content="Need some coconuts")
        assert response["status"] == 200
        comment_id = response["body"]["id"]
        # get the comment
        url_comment = f"{self.url_comments}/{comment_id}"
        response_get = RestClient().send_request("get", session=self.session, url=url_comment, headers=HEADERS)

        ValidateResponse().validate_response(actual_response=response_get, method="get", expected_status_code=200,
                                             feature="comment")

    def test_update_comment(self):
        """
        Test to update a comment.
        :return:
        """
        project_created = TodoBase().create_project("Project comments")
        project_id = project_created["body"]["id"]
        LOGGER.info("Project ID be where the comment will be created: %s", project_id)
        response = self.create_comment(project_id=project_id, content="Need more information here")
        assert response["status"] == 200
        comment_id = response["body"]["id"]
        response = self.update_comment(comment_id=comment_id, content="Find information in another folder")
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="comment")

    def test_delete_comment(self):
        """
        Test to delete a comment.
        :return:
        """
        project_created = TodoBase().create_project("Project comments for delete")
        project_id = project_created["body"]["id"]
        self.projects_list.append(project_id)
        LOGGER.info("Project ID be where the comment will be created: %s", project_id)
        response = self.create_comment(project_id=project_id, content="Need more information here")
        assert response["status"] == 200
        comment_id = response["body"]["id"]
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_comment)

        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="comment")

    def create_comment(self, project_id=None, task_id=None, content=None):
        """
        Method to create a comment
        :param project_id:
        :param task_id:
        :param content:
        :return:
        """
        data = {
            "content": content
        }
        if project_id:
            data["project_id"] = project_id
        if task_id:
            data["task_id"] = task_id
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_comments, data=data)
        return response

    def update_comment(self, comment_id=None, content=None):
        """
        Method to update a comment
        :param self:
        :param comment_id:
        :param content:
        :return:
        """
        data = {
            "content": content
        }
        url_comment = f"{self.url_comments}/{comment_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_comment, data=data)
        return response

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects and tasks created
        LOGGER.info("The following tasks will be deleted: %s", cls.tasks_list)
        TodoBase().delete_projects(cls.projects_list)
        TodoBase().delete_tasks(cls.tasks_list)
