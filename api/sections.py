import logging
import unittest

import requests

from api.todo_base import TodoBase
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient
from api.validate_response import ValidateResponse

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):
    """
    Class  for sections endpoint
    """

    @classmethod
    def setUpClass(cls):
        """
                Setup Class only executed one time
        """
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()
        cls.projects_list = []

    def test_create_section(self):
        """
        Test to create session
        :return:
        """
        project_created = TodoBase().create_project("Project Section")
        project_id = project_created["body"]["id"]
        data = {
            "project_id": project_id,
            "name": "Section 2"
        }
        self.projects_list.append(project_id)
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="section")

    def test_get_all_sections(self):
        """
        Test to get all sections
        :return:
        """
        response = TodoBase().get_all_sections()
        LOGGER.info("Number of sections returned: %s", len(response))
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="sections")

    def test_get_all_sections_by_project(self):
        """
        Test to get all sections of a specific project.
        :return:
        """
        project_created = TodoBase().create_project("MultipleSections")
        project_id = project_created["body"]["id"]
        TodoBase().create_sections(["section001", "section002", "section003"], project_id)
        url_section = f"{self.url_section}?project_id={project_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        LOGGER.info("Number of sections returned: %s", response)
        self.projects_list.append(project_id)
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="sections")

    def test_get_section(self):
        """
        Test to get a section
        :return:
        """
        response = TodoBase().get_all_sections()
        response_body = response["body"]
        section_id = response_body[1]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        response = response["body"]
        ValidateResponse().validate_response(actual_response=response, method="get", expected_status_code=200,
                                             feature="section")

    def test_delete_section(self):
        """
        Test to delete a section
        :return:
        """
        response = TodoBase().get_all_sections()
        response_body = response["body"]
        section_id = response_body[1]["id"]
        LOGGER.info("Section Id to be deleted: %s", section_id)
        LOGGER.info("Section name to be deleted: %s", response_body[1]["name"])
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("delete", session=self.session, headers=HEADERS,
                                             url=url_section)
        response = response["body"]
        ValidateResponse().validate_response(actual_response=response, method="delete", expected_status_code=204,
                                             feature="section")

    def test_update_section(self):
        """
        Test to update a section
        :return:
        """
        project_created = TodoBase().create_project("Project004")
        project_id = project_created["body"]["id"]
        section_id_list = TodoBase().create_sections(["section_010"], project_id)

        data = {
            "project_id": project_id,
            "order": 3,
            "name": "Section Updated"
        }
        self.projects_list.append(project_id)
        url_section = f"{self.url_section}/{section_id_list[0]}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section, data=data)
        ValidateResponse().validate_response(actual_response=response, method="post", expected_status_code=200,
                                             feature="section")

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
        # delete projects created
        TodoBase().delete_projects(cls.projects_list)
