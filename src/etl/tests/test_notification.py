import os
from unittest import mock
from etl.main import send_failure_email

@mock.patch("smtplib.SMTP")
@mock.patch.dict(os.environ, {
    "RECIPIENT_EMAIL": "to@example.com",
    "SENDER_EMAIL": "from@example.com",
    "SENDER_DATA": "dummy_password"
})
def test_send_failure_email(mock_smtp):
    smtp_instance = mock_smtp.return_value.__enter__.return_value
    smtp_instance.sendmail = mock.Mock()

    send_failure_email("Test error message")

    smtp_instance.sendmail.assert_called_once()
