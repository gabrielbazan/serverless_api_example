from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Type
from unittest import TestCase

import requests
from aws import query_rest_api_url

TODOS_URL_PATH = "todos"


class ListKey(str, Enum):
    RESULTS = "results"
    TOTAL_COUNT = "totalCount"
    COUNT = "count"


class ToDoKey(str, Enum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TASK = "task"
    DONE = "done"


class ToDosTestCase(TestCase):
    def setUp(self) -> None:
        self.api_url: str = query_rest_api_url()

        self.todos_uri: str = f"{self.api_url}/{TODOS_URL_PATH}"

    def test_list(self) -> None:
        self.do_test_endpoint(requests.get, self.todos_uri, 200, enum=ListKey)

    def test_create_and_read_and_delete(self) -> None:
        todo = {ToDoKey.TASK.value: "do something"}

        status_code, response_body = self.call_endpoint(
            requests.post, self.todos_uri, json=todo
        )
        self.assertEqual(status_code, 201)

        assert response_body is not None, "Creation endpoint hasn't returned data"

        self.assert_has_keys(response_body, ToDoKey)

        todo_id = response_body[ToDoKey.ID.value]

        todo_uri = f"{self.todos_uri}/{todo_id}"

        self.do_test_endpoint(requests.get, todo_uri, 200, enum=ToDoKey)

        self.do_test_endpoint(requests.delete, todo_uri, 204)

        self.do_test_endpoint(requests.get, todo_uri, 404)

    def do_test_endpoint(
        self,
        request_method: Callable,  # type: ignore
        uri: str,
        expected_status_code: int,
        enum: Optional[Type[Enum]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> None:
        status_code, response_body = self.call_endpoint(request_method, uri, json=json)
        self.assertEqual(status_code, expected_status_code)

        if enum:
            assert response_body is not None, "Expected to retrieve data from endpoint"
            self.assert_has_keys(response_body, enum)

    def call_endpoint(
        self,
        request_method: Callable,  # type: ignore
        uri: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Tuple[int, Optional[Dict[str, Any]]]:
        response = request_method(uri, json=json)

        response_json = None

        if response.text:
            response_json = response.json()

        return response.status_code, response_json

    def assert_has_keys(self, obj: Dict[str, Any], enum: Type[Enum]) -> None:
        for key in enum:
            self.assertIn(key.value, obj)
