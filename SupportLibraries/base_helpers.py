"""
This module contains common reusable functions.
"""

from traceback import print_stack
from SupportLibraries.ui_helpers import UIHelpers
from configparser import ConfigParser
import imaplib
import email
import re


class BaseHelpers(UIHelpers):
    """
    This class includes basic reusable base_helpers.
    """

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def load_properties_file(self):
        """
        This method loads the properties/ini file
        :return: this method returns config reader instance.
        """

        config = None
        try:
            # noinspection PyBroadException
            config = ConfigParser()
            config.read('test.ini')

        except Exception as ex:
            self.log.error("Failed to load ini/properties file.", ex)
            print_stack()

        return config

    def get_body(self, msg):
        """
        This method is used to get the mail body
        :param msg: input parameter as raw message
        :return: it returns the mail body according to content type
        """

        for part in msg.walk():
            con_type = part.get_content_type()

            if con_type == 'text/html':
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload
            elif con_type == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload
            elif con_type == 'multipart/mixed':
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload
            elif con_type == 'multipart/alternative':
                payload = part.get_payload(decode=True)
                if payload is not None:
                    return payload
            else:
                return None

    def get_reset_password_url(self, host, username, password, subject, site_url):
        """
        This method is used to get the reset password link from mail
        :param host: imap ssl host name
        :param username: email id of the user
        :param password: password for registered email id to log into mail
        :param subject: query parameter to search for specific subject in mails
        :param site_url: website url to reset the password for
        :return: it returns the password reset url
        """
        token_value = ""
        try:
            
            # Connect to the server
            print('Connecting to ' + host)
            mail = imaplib.IMAP4_SSL(host)

            # Login to our account
            mail.login(username, password)

            mail_list = mail.list()
            # print(mail_list)

            mail.select()
            search_query = '(SUBJECT "'+subject+'")'
            result, data = mail.uid('search', None, search_query)
            ids = data[0]

            # list of uids
            id_list = ids.split()

            i = len(id_list)
            for x in range(i):
                if x == 0:
                    latest_email_uid = id_list[0]
                else:
                    latest_email_uid = id_list[i - x]

                # fetch the email body (RFC822) for the given ID
                result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = email_data[0][1]

                # converts byte literal to string removing b''
                raw_email_string = raw_email.decode('UTF-8')
                email_message = email.message_from_string(raw_email_string)

                final_payload = (self.get_body(email_message)).decode('UTF-8')

                if final_payload is not None:
                    pattern = re.compile('token=(.*)">')
                    token = pattern.findall(final_payload)
                    if len(token) != 0:
                        token_value = token[0]
                        mail.uid('STORE', latest_email_uid, '+FLAGS', '(\\Deleted)')
                        break

            mail.expunge()
            mail.close()
            mail.logout()

            if token_value != "":
                return site_url + "/password/reset?token=" + token_value
            else:
                return None

        except Exception as ex:
            self.log.error("Failed to get reset password link from mail.", ex)
            return None

    def clean_mailbox(self, host, username, password, subject):
        """
        This method is used to get the reset password link from mail
        :param host: imap ssl host name
        :param username: email id of the user
        :param password: password for registered email id to log into mail
        :param subject: query parameter to search for specific subject in mails
        :return: returns boolean value for successful cleanup
        """
        token_value = ""
        try:

            # Connect to the server
            print('Connecting to ' + host)
            mail = imaplib.IMAP4_SSL(host)

            # Login to our account
            mail.login(username, password)

            mail_list = mail.list()
            # print(mail_list)

            mail.select()
            search_query = '(SUBJECT "' + subject + '")'
            result, data = mail.uid('search', None, search_query)
            ids = data[0]

            # list of uids
            id_list = ids.split()

            i = len(id_list)
            for x in range(i):
                if x == 0:
                    latest_email_uid = id_list[0]
                else:
                    latest_email_uid = id_list[i - x]

                mail.uid('STORE', latest_email_uid, '+FLAGS', '(\\Deleted)')

            mail.expunge()
            mail.close()
            mail.logout()

            self.log.info("Cleaned up all mail with subject as: " + subject)
            return True
        except Exception as ex:
            self.log.error("Failed to get reset password link from mail.", ex)
            return False
