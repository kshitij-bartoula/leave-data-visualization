import pytest
from unittest import mock
from etl.main import send_failure_email


@pytest.fixture
def mock_smtp():
    # Mock the smtplib.SMTP class to avoid actual email sending
    with mock.patch("smtplib.SMTP") as mock_smtp:
        yield mock_smtp


def test_send_failure_email(mock_smtp):
    # Mock the email sending
    mock_smtp.return_value.__enter__.return_value.sendmail = mock.Mock()

    # Call the function to send an email
    send_failure_email("Test error message")

    # Assert that the sendmail method was called once
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()
