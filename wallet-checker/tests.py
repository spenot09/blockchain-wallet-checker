# Standard library imports...
from unittest.mock import Mock, patch
from helpful_scripts import api_call()

# Third-party imports...
from nose.tools import assert_is_not_none


@patch("helpful_scripts.requests.get")
def test_getting_todos(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_todos()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)
