#!venv/bin/python
# import os
import unittest
# import tempfile

from app.constants import DATE_TIME_NOW
from app import emails
from app.models import User
import config


class TestEmail(unittest.TestCase):
    userEmail = "cldershem@gmail.com"
    adminEmail = config.ADMINS[0]
    subject = "This be a test."
    bodyText = ("This test was started at '{0}'.  \
                This email was sent at '{1}'.".format(
                DATE_TIME_NOW, DATE_TIME_NOW))
    bodyHTML = ("This test was started at <b>'{0}'</b>.  \
                This email was sent at <b>'{0}'</b>.".format(
                DATE_TIME_NOW, DATE_TIME_NOW))

    def setUp(self):
        config.TESTING = True

    def tearDown(self):
        pass

#     def test_send_email(self):
#         emails.send_email(
#             self.testSubject,
#             [self.adminEmail, self.userEmail],
#             [self.adminEmail, self.userEmail],
#             self.bodyText,
#             self.bodyHTML)

#     def test_send_email_async(self):
#         emails.send_email(
#             self.testSubject,
#             [self.adminEmail, self.userEmail],
#             [self.adminEmail, self.userEmail],
#             self.bodyText,
#             self.bodyHTML)

    def test_send_email_confirmirmation(self):
        user = User.get(email=self.userEmail)
        emails.email_confirmation(user, "payload")

    def test_send_password_reset(self):
        pass

if __name__ == '__main__':
    unittest.main()
