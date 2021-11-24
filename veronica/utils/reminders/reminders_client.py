"""
Taken from https://github.com/jonahar/google-reminders-cli and slightly adapted for use here.
"""

from datetime import datetime, timedelta
import json
from typing import List, Optional

import veronica.utils.reminders.reminders_client_utils as client_utils
from veronica.utils.reminders.reminder import Reminder, gen_id

HEADERS = {
    'content-type': 'application/json+protobuf',
}

HTTP_OK = 200


class RemindersClient:
    def __init__(self,SCOPES):
        self.auth_http = client_utils.authenticate(SCOPES)
    
    @staticmethod
    def _report_error(response, content, func_name: str):
        print(f'Error in {func_name}:')
        print(f'    status code: {response.status}')
        print(f'    content: {content}')
    
    def create_reminder(self, dt, title) -> bool:
        """
        send a 'create reminder' request.
        returns True upon a successful creation of a reminder
        """
        response, content = self.auth_http.request(
            uri='https://reminders-pa.clients6.google.com/v1internalOP/reminders/create',
            method='POST',
            body=client_utils.create_req_body({
                "dt": dt,
                "title": title,
                "id": gen_id()
            }),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            return True
        else:
            self._report_error(response, content, 'create_reminder')
            return False
    
    def delete_reminder(self, reminder_id: str) -> bool:
        """
        delete the reminder with the given id.
        Returns True upon a successful deletion
        """
        response, content = self.auth_http.request(
            uri='https://reminders-pa.clients6.google.com/v1internalOP/reminders/delete',
            method='POST',
            body=client_utils.delete_req_body(reminder_id),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            return True
        else:
            self._report_error(response, content, 'delete_reminder')
            return False
    
    def list_reminders(self: int,hours_upto) -> Optional[List[Reminder]]:
        """
        returns a list of the last num_reminders created reminders, or
        None if an error occurred
        """
        response, content = self.auth_http.request(
            uri='https://reminders-pa.clients6.google.com/v1internalOP/reminders/list',
            method='POST',
            body=client_utils.list_req_body(num_reminders=2500),
            headers=HEADERS,
        )
        if response.status == HTTP_OK:
            content_dict = json.loads(content.decode('utf-8'))
            if '1' not in content_dict:
                return []
            reminders_dict_list = content_dict['1']
            reminders = [
                client_utils.build_reminder(reminder_dict)
                for reminder_dict in reminders_dict_list
            ]
            return [
                i for i in reminders if datetime.now() < i["start"] < datetime.now() + timedelta(hours=hours_upto)
            ]
        else:
            self._report_error(response, content, 'list_reminders')
            return None
