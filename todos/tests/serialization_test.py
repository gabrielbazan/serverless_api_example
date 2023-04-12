from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from todos import serialization
from todos.aws import Lambda
from todos.http import StatusCode
from todos.serialization import (
    build_error_response,
    build_response,
    validate_request_body,
)

MODULE = "todos.serialization"


class SerializationTestCase(TestCase):
    @patch(f"{MODULE}.json")
    def test_validate_request_body_success(self, json: MagicMock) -> None:
        # Given
        body_str = Mock()
        event = MagicMock()
        event.__getitem__.return_value = body_str

        body_dict = {"test": 123}
        json.loads.return_value = body_dict

        model_type = MagicMock()
        model_instance = MagicMock()
        model_dict = Mock()
        model_type.return_value = model_instance
        model_instance.to_dict.return_value = model_dict

        # When
        data, errors = validate_request_body(event, model_type)

        # Then
        event.__getitem__.assert_called_once_with(Lambda.Event.BODY)
        json.loads.assert_called_once_with(body_str)
        model_type.assert_called_once_with(**body_dict)
        model_instance.to_dict.assert_called_once()

        self.assertIs(data, model_dict)
        self.assertIsNone(errors)

    @patch(f"{MODULE}.build_error_response")
    @patch(f"{MODULE}.json")
    def test_validate_request_body_error(
        self,
        json: MagicMock,
        build_error_response: MagicMock,
    ) -> None:
        # Given
        body_str = Mock()
        event = MagicMock()
        event.__getitem__.return_value = body_str

        body_dict = {"test": 123}
        json.loads.return_value = body_dict

        exception_errors = Mock()

        class ValidationError(Exception):
            def errors(self) -> Mock:
                return exception_errors

        serialization.ValidationError = ValidationError  # type: ignore

        model_type = MagicMock()
        model_type.side_effect = ValidationError

        errors = Mock()
        build_error_response.return_value = errors

        # When
        data, returned_errors = validate_request_body(event, model_type)

        # Then
        event.__getitem__.assert_called_once_with(Lambda.Event.BODY)
        json.loads.assert_called_once_with(body_str)
        model_type.assert_called_once_with(**body_dict)

        build_error_response.assert_called_once_with(
            StatusCode.BAD_REQUEST, exception_errors
        )

        self.assertIsNone(data)
        self.assertIs(errors, returned_errors)

    @patch(f"{MODULE}.build_response")
    def test_build_error_response(self, build_response_mock: MagicMock) -> None:
        # Given
        status_code, error = Mock(), Mock()

        response = Mock()

        build_response_mock.return_value = response

        # When
        returned_response = build_error_response(status_code, error)

        # Then
        build_response_mock.assert_called_once()
        self.assertIs(returned_response, response)

    def test_build_response(self) -> None:
        # Given
        status_code, body = Mock(), Mock()

        # When
        response = build_response(status_code, body)

        # Then
        self.assertIsInstance(response, dict)
